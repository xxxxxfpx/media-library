import asyncio
from database import AsyncSessionLocal
from database.models import File, FileLink
from sqlalchemy import select

async def check():
    async with AsyncSessionLocal() as db:
        for item_id in [47, 26402]:
            result = await db.execute(
                select(File, FileLink)
                .join(FileLink, FileLink.FileId == File.Id)
                .where(FileLink.ItemId == item_id)
            )
            files = result.all()
            print(f'媒体项 {item_id}:')
            for file, file_link in files:
                filename = file.Name or file.Path.split('/')[-1]
                img_type = file_link.ImageType or "视频"
                print(f'  {filename}: {file.Type} ({img_type})')
            print()

asyncio.run(check())
