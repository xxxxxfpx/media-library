"""
迁移 OriginalTitle 到 Alias 表
将远程 MediaItem 的 OriginalTitle 存入本地 Alias 表，Source='original'
"""
import os
import asyncio
import asyncpg
from database.core import AsyncSessionLocal
from database.models import Alias
from sqlalchemy import select


REMOTE_DB_CONFIG = {
    'host': os.environ.get('REMOTE_DB_HOST', ''),
    'port': int(os.environ.get('REMOTE_DB_PORT', '5432')),
    'database': os.environ.get('REMOTE_DB_NAME', ''),
    'user': os.environ.get('REMOTE_DB_USER', ''),
    'password': os.environ.get('REMOTE_DB_PASSWORD', '')
}


async def migrate_original_titles():
    """将远程 OriginalTitle 迁移到 Alias 表"""
    print("=" * 60)
    print("迁移 OriginalTitle 到 Alias 表 (Source='original')")
    print("=" * 60)

    remote_conn = await asyncpg.connect(**REMOTE_DB_CONFIG)
    print("✅ 远程数据库连接成功")

    async with AsyncSessionLocal() as local_session:
        # 获取远程有 OriginalTitle 的 MediaItems
        print("\n查询远程有 OriginalTitle 的 MediaItems...")
        rows = await remote_conn.fetch('''
            SELECT "Id", "Name", "OriginalTitle"
            FROM "MediaItems"
            WHERE "OriginalTitle" IS NOT NULL
            AND "OriginalTitle" != ''
            AND "OriginalTitle" != "Name"
        ''')
        print(f"远程有 OriginalTitle 的记录: {len(rows)}")

        if len(rows) == 0:
            print("没有需要迁移的 OriginalTitle")
            await remote_conn.close()
            return

        # 显示示例
        print("\n示例数据:")
        for row in rows[:5]:
            print(f"  ID={row['Id']}: Name='{row['Name']}' -> OriginalTitle='{row['OriginalTitle']}'")

        # 迁移
        print("\n开始迁移...")
        created = 0
        skipped = 0
        errors = 0

        for row in rows:
            try:
                # 检查是否已存在
                result = await local_session.execute(
                    select(Alias).where(
                        Alias.ItemId == row['Id'],
                        Alias.Name == row['OriginalTitle'],
                        Alias.Source == 'original'
                    )
                )
                existing = result.scalar_one_or_none()

                if existing:
                    skipped += 1
                    continue

                # 创建 Alias
                alias = Alias(
                    ItemId=row['Id'],
                    Name=row['OriginalTitle'],
                    Source='original'
                )
                local_session.add(alias)
                created += 1

                if created % 500 == 0:
                    await local_session.commit()
                    print(f"  已创建 {created} 个Alias")

            except Exception as e:
                errors += 1
                if errors <= 5:
                    print(f"  ⚠️  ID={row['Id']} 错误: {e}")
                await local_session.rollback()
                continue

        await local_session.commit()

        print(f"\n迁移完成:")
        print(f"  ✅ 新建: {created} 个")
        print(f"  ⏭️  跳过: {skipped} 个")
        print(f"  ❌ 错误: {errors} 个")

        # 验证
        print("\n验证 Alias 表:")
        from sqlalchemy import func
        total = (await local_session.execute(select(func.count()).select_from(Alias))).scalar_one()
        original_count = (await local_session.execute(
            select(func.count()).select_from(Alias).where(Alias.Source == 'original')
        )).scalar_one()
        print(f"  Alias 总数: {total}")
        print(f"  Source='original': {original_count}")

    await remote_conn.close()
    print("\n✅ 迁移完成!")


if __name__ == '__main__':
    asyncio.run(migrate_original_titles())