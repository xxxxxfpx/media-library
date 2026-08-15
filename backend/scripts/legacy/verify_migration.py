"""验证 item 3102 的迁移结果"""
import asyncio
from database.core import AsyncSessionLocal
from database.models import MediaItem, File, FileLink, ItemLinks
from sqlalchemy import select


async def main():
    async with AsyncSessionLocal() as db:
        # 检查 MediaItem
        result = await db.execute(select(MediaItem).where(MediaItem.Id == 3102))
        item = result.scalar_one_or_none()
        if item:
            print(f'✅ MediaItem: {item.Name} (ID={item.Id})')
            print(f'   Type: {item.Type.value}')
            print(f'   Overview: {item.Overview[:50]}...' if item.Overview else '   Overview: None')
        
        # 检查 Files
        print(f'\n📁 Files (通过 FileLink 关联):')
        result = await db.execute(
            select(File, FileLink).join(FileLink, FileLink.FileId == File.Id).where(FileLink.ItemId == 3102)
        )
        for file, link in result.all():
            print(f'  - FileId: {file.Id}')
            print(f'    Path: {file.Path}')
            print(f'    Type: {file.Type.value}, Size: {file.Size}')
            print(f'    ImageType: {link.ImageType.value if link.ImageType else "N/A"}, Index: {link.ImageIndex}')
            print()
        
        # 检查 ItemLinks (Genre/Studio/Tag/Person/Source)
        print(f'\n🔗 ItemLinks:')
        result = await db.execute(select(ItemLinks).where(ItemLinks.ItemId == 3102))
        links = result.scalars().all()
        
        genre_links = [l for l in links if l.Type.value == 'Genre']
        studio_links = [l for l in links if l.Type.value == 'Studio']
        tag_links = [l for l in links if l.Type.value == 'Tag']
        person_links = [l for l in links if l.Type.value == 'Person']
        source_links = [l for l in links if l.Type.value == 'Source']
        
        print(f'  Genre: {len(genre_links)} 个')
        print(f'  Studio: {len(studio_links)} 个')
        print(f'  Tag: {len(tag_links)} 个')
        print(f'  Person: {len(person_links)} 个')
        print(f'  Source: {len(source_links)} 个')
        
        for link in source_links:
            print(f'    - SourceId: {link.LinkedItemId}')
        
        print(f'\n✅ 验证完成！')


if __name__ == '__main__':
    asyncio.run(main())
