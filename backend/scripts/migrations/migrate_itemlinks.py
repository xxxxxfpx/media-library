"""
ItemLinks 迁移脚本

从远程 PostgreSQL 迁移媒体关联关系到本地 SQLite。
只迁移 ItemLinks 和 ItemProviders，跳过 ItemPeople（已弃用）和 ItemSources（已通过 FileLink 迁移）。

用法: python scripts/migrate_itemlinks.py
"""

import asyncio
import os
import sys

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

import asyncpg
from sqlalchemy import select
from database.core import AsyncSessionLocal
from database.models import MediaItem, ItemLinks

REMOTE_DB_CONFIG = {
    'host': os.environ.get('REMOTE_DB_HOST', ''),
    'port': int(os.environ.get('REMOTE_DB_PORT', '5432')),
    'database': os.environ.get('REMOTE_DB_NAME', ''),
    'user': os.environ.get('REMOTE_DB_USER', ''),
    'password': os.environ.get('REMOTE_DB_PASSWORD', ''),
}

BATCH_SIZE = 2000


class ItemLinksMigration:
    def __init__(self):
        self.remote_conn = None
        self.local_ids: set[int] = set()
        self.stats = {
            'item_links_total': 0,
            'item_links_skipped': 0,
            'item_links_inserted': 0,
            'item_providers_total': 0,
            'item_providers_skipped': 0,
            'item_providers_inserted': 0,
        }

    async def connect(self):
        print("🔗 连接远程 PostgreSQL...")
        self.remote_conn = await asyncpg.connect(**REMOTE_DB_CONFIG)
        print("✅ 远程连接成功")

    async def disconnect(self):
        if self.remote_conn:
            await self.remote_conn.close()
            print("🔗 远程连接已关闭")

    async def load_local_ids(self, db):
        """加载本地所有 MediaItem ID"""
        r = await db.execute(select(MediaItem.Id))
        self.local_ids = {row[0] for row in r.all()}
        print(f"📋 本地 MediaItem 共 {len(self.local_ids)} 个")

    def exists_locally(self, item_id: int) -> bool:
        return item_id in self.local_ids

    async def migrate_item_links(self, db):
        """迁移 ItemLinks（通用关联：Genre/Studio/Tag/BoxSet/层级关系）"""
        print("\n🔗 迁移 ItemLinks...")

        offset = 0
        total = 0

        while True:
            rows = await self.remote_conn.fetch(
                '''SELECT "ItemId", "LinkedItemId"
                   FROM "ItemLinks"
                   ORDER BY "ItemId", "LinkedItemId"
                   LIMIT $1 OFFSET $2''',
                BATCH_SIZE, offset
            )

            if not rows:
                break

            for row in rows:
                self.stats['item_links_total'] += 1
                item_id = row['ItemId']
                linked_id = row['LinkedItemId']

                # 跳过自关联
                if item_id == linked_id:
                    self.stats['item_links_skipped'] += 1
                    continue

                # 检查两端是否都在本地存在
                if not self.exists_locally(item_id) or not self.exists_locally(linked_id):
                    self.stats['item_links_skipped'] += 1
                    continue

                try:
                    link = ItemLinks(
                        ItemId=item_id,
                        LinkedItemId=linked_id,
                    )
                    db.add(link)
                    await db.flush()
                    self.stats['item_links_inserted'] += 1
                except Exception:
                    # 唯一约束冲突或其它错误，跳过
                    await db.rollback()
                    self.stats['item_links_skipped'] += 1
                    continue

            offset += BATCH_SIZE
            total += len(rows)
            print(f"  进度: {total} 条, 已插入: {self.stats['item_links_inserted']}, 跳过: {self.stats['item_links_skipped']}", end='\r')

        await db.commit()
        print(f"\n  ✅ ItemLinks: 共 {self.stats['item_links_total']} 条, "
              f"插入 {self.stats['item_links_inserted']}, "
              f"跳过 {self.stats['item_links_skipped']}")

    async def migrate_item_providers(self, db):
        """迁移 ItemProviders（Item → Source 关联）"""
        print("\n📡 迁移 ItemProviders → Source 关联...")

        # 先获取 Provider → Source ID 映射
        providers = await self.remote_conn.fetch(
            'SELECT "Id", "Name" FROM "Providers"'
        )
        # Provider 的 Id 与本地 Source 的 Id 一致（迁移时保留了原 ID）
        provider_ids = {p['Id'] for p in providers if self.exists_locally(p['Id'])}
        print(f"  Providers: {len(provider_ids)} 个匹配本地 Source")

        offset = 0
        total = 0

        while True:
            rows = await self.remote_conn.fetch(
                '''SELECT "ItemId", "ProviderId", "SourceId"
                   FROM "ItemProviders"
                   ORDER BY "ItemId"
                   LIMIT $1 OFFSET $2''',
                BATCH_SIZE, offset
            )

            if not rows:
                break

            for row in rows:
                self.stats['item_providers_total'] += 1
                item_id = row['ItemId']
                provider_id = row['ProviderId']
                source_id = row['SourceId']

                # ProviderId 需要映射为本地 Source ID
                source_local_id = provider_id
                if source_local_id not in provider_ids:
                    self.stats['item_providers_skipped'] += 1
                    continue

                if not self.exists_locally(item_id):
                    self.stats['item_providers_skipped'] += 1
                    continue

                try:
                    link = ItemLinks(
                        ItemId=item_id,
                        LinkedItemId=source_local_id,
                        SourceId=source_id,
                    )
                    db.add(link)
                    await db.flush()
                    self.stats['item_providers_inserted'] += 1
                except Exception:
                    await db.rollback()
                    self.stats['item_providers_skipped'] += 1
                    continue

            offset += BATCH_SIZE
            total += len(rows)
            print(f"  进度: {total} 条, 已插入: {self.stats['item_providers_inserted']}, 跳过: {self.stats['item_providers_skipped']}", end='\r')

        await db.commit()
        print(f"\n  ✅ ItemProviders: 共 {self.stats['item_providers_total']} 条, "
              f"插入 {self.stats['item_providers_inserted']}, "
              f"跳过 {self.stats['item_providers_skipped']}")

    async def run(self):
        print("=" * 60)
        print("ItemLinks 迁移工具")
        print("=" * 60)

        await self.connect()

        try:
            async with AsyncSessionLocal() as db:
                await self.load_local_ids(db)
                await self.migrate_item_links(db)
                await self.migrate_item_providers(db)

            print("\n" + "=" * 60)
            print("迁移完成统计")
            print("=" * 60)
            for key, count in self.stats.items():
                print(f"  {key:30s}: {count:6d}")
            inserted = self.stats['item_links_inserted'] + self.stats['item_providers_inserted']
            skipped = self.stats['item_links_skipped'] + self.stats['item_providers_skipped']
            print(f"  {'总计插入':30s}: {inserted:6d}")
            print(f"  {'总计跳过':30s}: {skipped:6d}")
            print("✅ 迁移完成！")

        except Exception as e:
            print(f"\n❌ 迁移失败: {e}")
            import traceback
            traceback.print_exc()
        finally:
            await self.disconnect()


if __name__ == '__main__':
    asyncio.run(ItemLinksMigration().run())
