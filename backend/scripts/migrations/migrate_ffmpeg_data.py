"""
迁移 FFmpeg 数据到本地数据库
将远程 PostgreSQL Files.Data 字段存入本地 Files.FFmpeg 字段
"""
import os
import asyncio
import asyncpg
import json
from database.core import AsyncSessionLocal
from database.models import File
from sqlalchemy import select


REMOTE_DB_CONFIG = {
    'host': os.environ.get('REMOTE_DB_HOST', ''),
    'port': int(os.environ.get('REMOTE_DB_PORT', '5432')),
    'database': os.environ.get('REMOTE_DB_NAME', ''),
    'user': os.environ.get('REMOTE_DB_USER', ''),
    'password': os.environ.get('REMOTE_DB_PASSWORD', '')
}

BATCH_SIZE = 500


async def migrate_ffmpeg_data():
    """迁移 FFmpeg 数据"""
    print("=" * 60)
    print("迁移 FFmpeg 数据 (Files.Data → Files.FFmpeg)")
    print("=" * 60)

    remote_conn = await asyncpg.connect(**REMOTE_DB_CONFIG)
    print("✅ 远程数据库连接成功")

    # 获取远程有 Data 的文件数
    print("\n查询远程有 Data 的文件...")
    total_remote = await remote_conn.fetchval('SELECT COUNT(*) FROM "Files" WHERE "Data" IS NOT NULL')
    print(f"远程有 Data 的文件总数: {total_remote}")

    if total_remote == 0:
        print("没有需要迁移的 FFmpeg 数据")
        await remote_conn.close()
        return

    # 分批迁移
    print(f"\n开始迁移（每批 {BATCH_SIZE} 条）...")
    migrated = 0
    skipped = 0
    errors = 0
    offset = 0

    while True:
        rows = await remote_conn.fetch('''
            SELECT "Id", "Data"
            FROM "Files"
            WHERE "Data" IS NOT NULL
            ORDER BY "Id"
            LIMIT $1 OFFSET $2
        ''', BATCH_SIZE, offset)

        if not rows:
            break

        async with AsyncSessionLocal() as local_session:
            for row in rows:
                try:
                    # 检查本地文件是否存在
                    result = await local_session.execute(
                        select(File).where(File.Id == row['Id'])
                    )
                    local_file = result.scalar_one_or_none()

                    if not local_file:
                        skipped += 1
                        continue

                    # 如果已有 FFmpeg 数据，跳过
                    if local_file.FFmpeg:
                        skipped += 1
                        continue

                    # 转换 Data 为 JSON 字符串
                    ff_data = None
                    if row['Data']:
                        try:
                            if isinstance(row['Data'], dict):
                                ff_data = json.dumps(row['Data'], ensure_ascii=False)
                            else:
                                ff_data = str(row['Data'])
                        except:
                            ff_data = str(row['Data'])

                    # 更新本地文件
                    await local_session.execute(
                        select(File).where(File.Id == row['Id'])
                    )
                    from sqlalchemy import update
                    await local_session.execute(
                        update(File)
                        .where(File.Id == row['Id'])
                        .values(FFmpeg=ff_data)
                    )
                    migrated += 1

                except Exception as e:
                    errors += 1
                    if errors <= 3:
                        print(f"  ⚠️  ID={row['Id']} 错误: {e}")

            await local_session.commit()

        offset += BATCH_SIZE
        print(f"  进度: 已迁移 {migrated} 条, 跳过 {skipped} 条, 错误 {errors} 条")

        if len(rows) < BATCH_SIZE:
            break

    print(f"\n迁移完成:")
    print(f"  ✅ 成功: {migrated} 条")
    print(f"  ⏭️  跳过: {skipped} 条")
    print(f"  ❌ 错误: {errors} 条")

    await remote_conn.close()
    print("\n✅ FFmpeg 数据迁移完成!")


if __name__ == '__main__':
    asyncio.run(migrate_ffmpeg_data())