"""
全量数据迁移脚本

从远程 PostgreSQL 迁移所有数据到本地 SQLite。
自动清空现有数据后重新迁移。

用法: python scripts/full_migrate.py
"""

import asyncio
import asyncpg
import json
import os
import sys
from datetime import datetime, timezone
from typing import Optional

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from sqlalchemy import select, func, text
from sqlalchemy.ext.asyncio import AsyncSession
from database.core import AsyncSessionLocal, engine, init_db
from database.models import (
    Base, MediaItem, MediaType, ItemLinks, File, FileType,
    FileLink, ImageType, Alias, User, UserData,
)

# ── 配置 ──────────────────────────────────────────────────

REMOTE_DB = {
    'host': os.environ.get('REMOTE_DB_HOST', ''),
    'port': int(os.environ.get('REMOTE_DB_PORT', '5432')),
    'database': os.environ.get('REMOTE_DB_NAME', ''),
    'user': os.environ.get('REMOTE_DB_USER', ''),
    'password': os.environ.get('REMOTE_DB_PASSWORD', ''),
}

BATCH_SIZE = 1000

# 远程类型 → 本地 MediaType 映射（不迁移 Person/Source/CollectionFolder）
MEDIA_TYPE_MAP = {
    'Movie': MediaType.Movie,
    'Series': MediaType.Series,
    'Season': MediaType.Season,
    'Episode': MediaType.Episode,
    'Tag': MediaType.Tag,
    'Genre': MediaType.Genre,
    'Studio': MediaType.Studio,
    'BoxSet': MediaType.BoxSet,
}

FILE_TYPE_MAP = {
    'Video': FileType.Video,
    'Audio': FileType.Audio,
    'Image': FileType.Image,
    'Subtitle': FileType.Subtitle,
}

IMAGE_TYPE_MAP = {
    'Primary': ImageType.Primary,
    'Backdrop': ImageType.Backdrop,
    'Logo': ImageType.Logo,
    'Thumb': ImageType.Thumb,
    'Screenshot': ImageType.Screenshot,
    'Chapter': ImageType.Chapter,
    'Art': ImageType.Art,
    'Banner': ImageType.Banner,
    'Disc': ImageType.Disc,
    'Box': ImageType.Box,
    'BoxRear': ImageType.BoxRear,
    'Profile': ImageType.Profile,
    'Menu': ImageType.Menu,
}


# ── 工具 ──────────────────────────────────────────────────

def to_utc(dt) -> Optional[datetime]:
    if dt is None:
        return None
    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt


# ── 迁移主类 ──────────────────────────────────────────────

class FullMigration:
    async def connect(self):
        print("🔗 连接远程 PostgreSQL...")
        self.remote = await asyncpg.connect(**REMOTE_DB)
        print("✅ 远程连接成功")

    async def disconnect(self):
        if self.remote:
            await self.remote.close()
            print("🔗 远程连接已关闭")

    # ── 清库 ──────────────────────────────────────────────

    async def clear_database(self):
        """清空所有数据表"""
        print("\n🗑️  清空数据库...")
        async with AsyncSessionLocal() as db:
            # 按外键依赖顺序删除
            for table in ['Aliases', 'UserData', 'FileLinks', 'ItemLinks', 'Files', 'MediaItems', 'Users']:
                await db.execute(text(f'DELETE FROM "{table}"'))
            await db.commit()
        print("✅ 数据库已清空")

    # ── 批量插入辅助 ───────────────────────────────────────

    async def batch_insert(self, db, records, batch_size=BATCH_SIZE):
        """批量添加并提交"""
        for i in range(0, len(records), batch_size):
            batch = records[i:i + batch_size]
            for rec in batch:
                db.add(rec)
            await db.flush()
        await db.commit()

    async def fetch_count(self, table: str) -> int:
        return await self.remote.fetchval(f'SELECT COUNT(*) FROM "{table}"')

    # ── 1. MediaItems ─────────────────────────────────────

    def __init__(self):
        self.remote = None
        self.stats = {}
        self.provider_mapping = {}  # 远程 ProviderId → 本地 Source ID

    async def migrate_media_items(self):
        """迁移所有 MediaItems（排除 Person）"""
        print("\n🎬 迁移 MediaItems...")
        count = await self.fetch_count('MediaItems')
        print(f"  远程总数: {count}")

        offset = 0
        all_items = []
        while True:
            rows = await self.remote.fetch(f'''
                SELECT "Id", "Type", "Name",
                       "Overview", "Tagline", "PremiereDate", "EndDate",
                       "OfficialRating", "CommunityRating", "CriticRating",
                       "DateCreated", "DateModified"
                FROM "MediaItems"
                ORDER BY "Id"
                LIMIT $1 OFFSET $2
            ''', BATCH_SIZE, offset)
            if not rows:
                break
            all_items.extend(rows)
            offset += BATCH_SIZE

        print(f"  读取 {len(all_items)} 条")

        async with AsyncSessionLocal() as db:
            inserted = 0
            skipped = 0
            for row in all_items:
                media_type = MEDIA_TYPE_MAP.get(row['Type'])
                if not media_type:
                    skipped += 1
                    continue

                item = MediaItem(
                    Id=row['Id'],
                    Type=media_type,
                    Name=row['Name'],
                    Overview=row['Overview'],
                    Tagline=row['Tagline'],
                    PremiereDate=to_utc(row['PremiereDate']),
                    EndDate=to_utc(row['EndDate']),
                    OfficialRating=row['OfficialRating'],
                    CommunityRating=row['CommunityRating'],
                    CriticRating=row['CriticRating'],
                    DateCreated=to_utc(row['DateCreated']) or datetime.now(timezone.utc),
                    DateModified=to_utc(row['DateModified']) or datetime.now(timezone.utc),
                )
                db.add(item)
                inserted += 1

                if inserted % BATCH_SIZE == 0:
                    await db.flush()

            await db.commit()
            self.stats['MediaItems'] = {'total': len(all_items), 'inserted': inserted, 'skipped': skipped}
            print(f"  ✅ MediaItems: 插入 {inserted}, 跳过(类型不支持) {skipped}")

    # ── 2. Providers → Source ──────────────────────────────

    async def migrate_providers(self):
        """迁移 Providers 为 Source（使用自增 ID）"""
        print("\n📦 迁移 Providers → Source...")
        rows = await self.remote.fetch('SELECT "Id", "Name" FROM "Providers"')

        provider_mapping = {}  # 旧 ProviderId → 新 Source ID

        async with AsyncSessionLocal() as db:
            for row in rows:
                item = MediaItem(
                    Type=MediaType.Source,
                    Name=row['Name'],
                    DateCreated=datetime.now(timezone.utc),
                    DateModified=datetime.now(timezone.utc),
                )
                db.add(item)
                await db.flush()
                provider_mapping[row['Id']] = item.Id

            await db.commit()
            self.stats['Sources'] = len(provider_mapping)
            self.provider_mapping = provider_mapping
            print(f"  ✅ Sources: 新增 {len(provider_mapping)} 个 (ID 映射: {provider_mapping})")

    # ── 3. Files ──────────────────────────────────────────

    async def migrate_files(self):
        """迁移所有 Files"""
        print("\n📁 迁移 Files...")
        count = await self.fetch_count('Files')
        print(f"  远程总数: {count}")

        offset = 0
        all_files = []
        while True:
            rows = await self.remote.fetch(f'''
                SELECT "Id", "Etag", "Size", "Name", "SortName",
                       "Path", "CloudId", "Type", "Data"
                FROM "Files"
                ORDER BY "Id"
                LIMIT $1 OFFSET $2
            ''', BATCH_SIZE, offset)
            if not rows:
                break
            all_files.extend(rows)
            offset += BATCH_SIZE

        print(f"  读取 {len(all_files)} 条")

        async with AsyncSessionLocal() as db:
            inserted = 0
            for row in all_files:
                file_type = FILE_TYPE_MAP.get(row['Type'], FileType.Video)

                ffmpeg = None
                if row['Data']:
                    try:
                        data = json.loads(row['Data'])
                        ffmpeg = json.dumps(data, ensure_ascii=False)
                    except (json.JSONDecodeError, TypeError):
                        pass

                f = File(
                    Id=row['Id'],
                    Etag=row['Etag'],
                    Size=row['Size'],
                    Name=row['Name'],
                    SortName=row['SortName'],
                    Path=row['Path'],
                    CloudId=row['CloudId'],
                    Type=file_type,
                    FFmpeg=ffmpeg,
                )
                db.add(f)
                inserted += 1

                if inserted % BATCH_SIZE == 0:
                    await db.flush()

            await db.commit()
            self.stats['Files'] = inserted
            print(f"  ✅ Files: 插入 {inserted}")

    # ── 4. FileLinks from FileImages ───────────────────────

    async def migrate_file_images(self):
        """迁移 FileImages → FileLink（图片关联）"""
        print("\n🖼️  迁移 FileImages → FileLink...")
        count = await self.fetch_count('FileImages')
        print(f"  远程总数: {count}")

        offset = 0
        all_links = []
        while True:
            rows = await self.remote.fetch(f'''
                SELECT "ItemId", "FileId", "Type", "ImageIndex"
                FROM "FileImages"
                ORDER BY "ItemId", "FileId"
                LIMIT $1 OFFSET $2
            ''', BATCH_SIZE, offset)
            if not rows:
                break
            all_links.extend(rows)
            offset += BATCH_SIZE

        print(f"  读取 {len(all_links)} 条")

        async with AsyncSessionLocal() as db:
            # 获取本地存在的 MediaItem ID 和 File ID
            existing_items = set()
            existing_files = set()
            r = await db.execute(select(MediaItem.Id))
            for row in r.all():
                existing_items.add(row[0])
            r = await db.execute(select(File.Id))
            for row in r.all():
                existing_files.add(row[0])

            inserted = 0
            skipped = 0
            for row in all_links:
                if row['ItemId'] not in existing_items or row['FileId'] not in existing_files:
                    skipped += 1
                    continue

                image_type = IMAGE_TYPE_MAP.get(row['Type'], ImageType.Primary)
                link = FileLink(
                    ItemId=row['ItemId'],
                    FileId=row['FileId'],
                    ImageType=image_type,
                    ImageIndex=row['ImageIndex'] or 0,
                )
                db.add(link)
                inserted += 1

                if inserted % BATCH_SIZE == 0:
                    await db.flush()

            await db.commit()
            self.stats['FileImages→FileLink'] = {'inserted': inserted, 'skipped': skipped}
            print(f"  ✅ FileLink(图片): 插入 {inserted}, 跳过 {skipped}")

    # ── 5. FileLinks from ItemSources ──────────────────────

    async def migrate_item_sources(self):
        """迁移 ItemSources → FileLink（视频文件关联）"""
        print("\n📡 迁移 ItemSources → FileLink...")
        count = await self.fetch_count('ItemSources')
        print(f"  远程总数: {count}")

        offset = 0
        all_links = []
        while True:
            rows = await self.remote.fetch(f'''
                SELECT "ItemId", "FileId", "Type"
                FROM "ItemSources"
                ORDER BY "ItemId", "FileId"
                LIMIT $1 OFFSET $2
            ''', BATCH_SIZE, offset)
            if not rows:
                break
            all_links.extend(rows)
            offset += BATCH_SIZE

        print(f"  读取 {len(all_links)} 条")

        async with AsyncSessionLocal() as db:
            existing_items = set()
            existing_files = set()
            r = await db.execute(select(MediaItem.Id))
            for row in r.all():
                existing_items.add(row[0])
            r = await db.execute(select(File.Id))
            for row in r.all():
                existing_files.add(row[0])

            inserted = 0
            skipped = 0
            for row in all_links:
                if row['ItemId'] not in existing_items or row['FileId'] not in existing_files:
                    skipped += 1
                    continue
                link = FileLink(
                    ItemId=row['ItemId'],
                    FileId=row['FileId'],
                    ImageType=None,
                    ImageIndex=0,
                )
                db.add(link)
                inserted += 1

                if inserted % BATCH_SIZE == 0:
                    await db.flush()

            await db.commit()
            self.stats['ItemSources→FileLink'] = {'inserted': inserted, 'skipped': skipped}
            print(f"  ✅ FileLink(视频): 插入 {inserted}, 跳过 {skipped}")

    # ── 6. ItemLinks（通用关联）────────────────────────────

    async def migrate_item_links(self):
        """迁移 ItemLinks（Genre/Studio/Tag/BoxSet/层级关联）"""
        print("\n🔗 迁移 ItemLinks...")
        count = await self.fetch_count('ItemLinks')
        print(f"  远程总数: {count}")

        offset = 0
        all_links = []
        while True:
            rows = await self.remote.fetch(f'''
                SELECT "ItemId", "LinkedItemId"
                FROM "ItemLinks"
                ORDER BY "ItemId", "LinkedItemId"
                LIMIT $1 OFFSET $2
            ''', BATCH_SIZE, offset)
            if not rows:
                break
            all_links.extend(rows)
            offset += BATCH_SIZE

        print(f"  读取 {len(all_links)} 条")

        async with AsyncSessionLocal() as db:
            existing_ids = set()
            r = await db.execute(select(MediaItem.Id))
            for row in r.all():
                existing_ids.add(row[0])

            inserted = 0
            skipped = 0
            for row in all_links:
                item_id = row['ItemId']
                linked_id = row['LinkedItemId']

                # 跳过自关联和不存在项
                if item_id == linked_id or item_id not in existing_ids or linked_id not in existing_ids:
                    skipped += 1
                    continue

                try:
                    link = ItemLinks(ItemId=item_id, LinkedItemId=linked_id)
                    db.add(link)
                    inserted += 1
                except Exception:
                    skipped += 1

                if inserted % BATCH_SIZE == 0:
                    await db.flush()

            await db.commit()
            self.stats['ItemLinks'] = {'total': len(all_links), 'inserted': inserted, 'skipped': skipped}
            print(f"  ✅ ItemLinks: 插入 {inserted}, 跳过 {skipped}")

    # ── 7. ItemProviders（Source 关联）─────────────────────

    async def migrate_item_providers(self):
        """迁移 ItemProviders → ItemLinks（Source 关联）"""
        print("\n🏢 迁移 ItemProviders → ItemLinks(Source)...")
        count = await self.fetch_count('ItemProviders')
        print(f"  远程总数: {count}")

        offset = 0
        all_links = []
        while True:
            rows = await self.remote.fetch(f'''
                SELECT "ItemId", "ProviderId", "SourceId", "Url"
                FROM "ItemProviders"
                ORDER BY "ItemId"
                LIMIT $1 OFFSET $2
            ''', BATCH_SIZE, offset)
            if not rows:
                break
            all_links.extend(rows)
            offset += BATCH_SIZE

        print(f"  读取 {len(all_links)} 条")

        async with AsyncSessionLocal() as db:
            existing_ids = set()
            r = await db.execute(select(MediaItem.Id))
            for row in r.all():
                existing_ids.add(row[0])

            inserted = 0
            skipped = 0
            for row in all_links:
                item_id = row['ItemId']
                provider_id = row['ProviderId']
                source_id = row['SourceId']

                # ProviderId → 本地 Source ID
                local_source_id = self.provider_mapping.get(provider_id)
                if item_id not in existing_ids or local_source_id is None:
                    skipped += 1
                    continue

                try:
                    link = ItemLinks(
                        ItemId=item_id,
                        LinkedItemId=local_source_id,
                        SourceId=source_id,
                        SourceLink=row.get('Url'),
                    )
                    db.add(link)
                    inserted += 1
                except Exception:
                    skipped += 1

                if inserted % BATCH_SIZE == 0:
                    await db.flush()

            await db.commit()
            self.stats['ItemProviders→ItemLinks'] = {'inserted': inserted, 'skipped': skipped}
            print(f"  ✅ ItemProviders: 插入 {inserted}, 跳过 {skipped}")

    # ── 8. 层级关联（Series→Season→Episode via ParentId）───

    async def migrate_hierarchy(self):
        """迁移 Series→Season→Episode 层级关系（从 ParentId）"""
        print("\n🏗️  迁移层级关联 (ParentId)...")

        season_links = await self.remote.fetch('''
            SELECT "Id", "ParentId" FROM "MediaItems"
            WHERE "Type" = 'Season' AND "ParentId" IS NOT NULL
        ''')
        episode_links = await self.remote.fetch('''
            SELECT "Id", "ParentId" FROM "MediaItems"
            WHERE "Type" = 'Episode' AND "ParentId" IS NOT NULL
        ''')

        async with AsyncSessionLocal() as db:
            r = await db.execute(select(MediaItem.Id))
            local_ids = {row[0] for row in r.all()}

            inserted = 0
            skipped = 0

            for row in season_links:
                season_id, series_id = row['Id'], row['ParentId']
                if season_id not in local_ids or series_id not in local_ids:
                    skipped += 1
                    continue
                try:
                    db.add(ItemLinks(ItemId=series_id, LinkedItemId=season_id))
                    inserted += 1
                except Exception:
                    skipped += 1
                    await db.rollback()

            for row in episode_links:
                episode_id, season_id = row['Id'], row['ParentId']
                if episode_id not in local_ids or season_id not in local_ids:
                    skipped += 1
                    continue
                try:
                    db.add(ItemLinks(ItemId=season_id, LinkedItemId=episode_id))
                    inserted += 1
                except Exception:
                    skipped += 1
                    await db.rollback()

            await db.commit()
            self.stats['Hierarchy'] = {'inserted': inserted, 'skipped': skipped}
            print(f"  ✅ 层级关联: 插入 {inserted}, 跳过 {skipped}")

    # ── 运行 ──────────────────────────────────────────────

    async def run(self):
        start = datetime.now()
        print("=" * 60)
        print("全量数据迁移")
        print("=" * 60)

        await self.connect()

        try:
            # 清库
            await self.clear_database()

            # 阶段 1: MediaItems（先迁移，避免与 Sources 自增 ID 冲突）
            await self.migrate_media_items()

            # 阶段 1b: Providers → Source（使用自增 ID，在 MediaItems 之后）
            await self.migrate_providers()

            # 阶段 2: Files
            await self.migrate_files()

            # 阶段 3: FileLinks
            await self.migrate_file_images()
            await self.migrate_item_sources()

            # 阶段 4: ItemLinks
            await self.migrate_item_links()
            await self.migrate_item_providers()
            await self.migrate_hierarchy()

            # 统计
            elapsed = datetime.now() - start
            print("\n" + "=" * 60)
            print("迁移完成统计")
            print("=" * 60)
            for key, val in self.stats.items():
                if isinstance(val, dict):
                    detail = ", ".join(f"{k}={v}" for k, v in val.items())
                    print(f"  {key:30s}: {detail}")
                else:
                    print(f"  {key:30s}: {val}")

            # 最终数据量
            async with AsyncSessionLocal() as db:
                for table in ['MediaItems', 'Files', 'FileLinks', 'ItemLinks', 'Aliases', 'UserData', 'Users']:
                    r = await db.execute(text(f'SELECT COUNT(*) FROM "{table}"'))
                    print(f"  {table:30s}: {r.scalar()}")

            print(f"\n⏱️  总耗时: {elapsed}")
            print("✅ 迁移完成！")

        except Exception as e:
            print(f"\n❌ 迁移失败: {e}")
            import traceback
            traceback.print_exc()
        finally:
            await self.disconnect()


if __name__ == '__main__':
    asyncio.run(FullMigration().run())
