"""检查 FFmpeg 数据"""
import asyncio
from database.core import AsyncSessionLocal
from database.models import File
from sqlalchemy import select, func

async def main():
    async with AsyncSessionLocal() as s:
        total = (await s.execute(select(func.count()).select_from(File))).scalar_one()
        print(f"Total files: {total}")

        has_ffmpeg = (await s.execute(
            select(func.count()).select_from(File).where(File.FFmpeg.isnot(None))
        )).scalar_one()
        print(f"Files with FFmpeg: {has_ffmpeg}")

        video_count = (await s.execute(
            select(func.count()).select_from(File).where(File.Type == 'Video')
        )).scalar_one()
        print(f"Video files: {video_count}")

        video_has_ffmpeg = (await s.execute(
            select(func.count()).select_from(File).where(
                File.Type == 'Video',
                File.FFmpeg.isnot(None)
            )
        )).scalar_one()
        print(f"Video files with FFmpeg: {video_has_ffmpeg}")

asyncio.run(main())