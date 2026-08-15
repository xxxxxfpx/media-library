"""检查数据库中 FFmpeg 数据和 Alias 表状态"""
import asyncio
from database.core import AsyncSessionLocal
from database.models import File
from sqlalchemy import select, func


async def check_ffmpeg_data():
    """检查 File.FFmpeg 数据"""
    print("=" * 60)
    print("检查 File.FFmpeg 数据")
    print("=" * 60)

    async with AsyncSessionLocal() as s:
        # 总文件数
        total = (await s.execute(select(func.count()).select_from(File))).scalar_one()
        print(f"\n总文件数: {total}")

        # 有 FFmpeg 数据的文件数
        has_ffmpeg = (await s.execute(
            select(func.count()).select_from(File).where(File.FFmpeg.isnot(None))
        )).scalar_one()
        print(f"有 FFmpeg 数据的文件数: {has_ffmpeg}")

        # 按 Type 统计
        print("\n按文件类型统计:")
        for file_type in ['Video', 'Image', 'Audio', 'Subtitle']:
            count = (await s.execute(
                select(func.count()).select_from(File).where(File.Type == file_type)
            )).scalar_one()
            has_ff = (await s.execute(
                select(func.count()).select_from(File).where(
                    File.Type == file_type,
                    File.FFmpeg.isnot(None)
                )
            )).scalar_one()
            print(f"  {file_type}: 总数={count}, 有FFmpeg={has_ff}")

        # 显示几个有 FFmpeg 数据的示例
        if has_ffmpeg > 0:
            print("\n有 FFmpeg 数据的文件示例:")
            samples = await s.execute(
                select(File.Id, File.Name, File.Type, File.FFmpeg)
                .where(File.FFmpeg.isnot(None))
                .limit(3)
            )
            for row in samples.all():
                print(f"  ID={row.Id}, Name={row.Name[:40]}, Type={row.Type}")
                ff_data = row.FFmpeg
                if ff_data:
                    print(f"    FFmpeg 数据长度: {len(str(ff_data))} 字符")
                    # 显示部分内容
                    ff_str = str(ff_data)
                    print(f"    FFmpeg 前100字符: {ff_str[:100]}...")


async def check_alias_table():
    """检查 Alias 表状态"""
    print("\n" + "=" * 60)
    print("检查 Alias 表")
    print("=" * 60)

    from database.models import Alias

    async with AsyncSessionLocal() as s:
        total = (await s.execute(select(func.count()).select_from(Alias))).scalar_one()
        print(f"\nAlias 总数: {total}")

        # 按 Source 统计
        print("\n按 Source 统计:")
        sources = await s.execute(select(Alias.Source, func.count()).group_by(Alias.Source))
        for row in sources.all():
            print(f"  Source='{row[0]}': {row[1]} 条")

        # 检查是否有 'original' 来源的
        original_count = (await s.execute(
            select(func.count()).select_from(Alias).where(Alias.Source == 'original')
        )).scalar_one()
        print(f"\nSource='original' 的数量: {original_count}")


async def main():
    await check_ffmpeg_data()
    await check_alias_table()


if __name__ == '__main__':
    asyncio.run(main())