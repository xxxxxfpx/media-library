"""
修复数据库中的文件类型
将 ImageType 为 Backdrop 或 Primary 的文件类型从 Video 改为 Image
"""

import asyncio
from database import AsyncSessionLocal
from database.models import File, FileLink
from database.models.enums import FileType, ImageType
from sqlalchemy import select, update


async def fix_file_types():
    """修复文件类型"""
    async with AsyncSessionLocal() as db:
        print("开始修复文件类型...")
        print()

        # 1. 查询所有 ImageType 为 Backdrop 或 Primary 的 FileLink
        result = await db.execute(
            select(FileLink, File)
            .join(File, File.Id == FileLink.FileId)
            .where(
                FileLink.ImageType.in_([ImageType.Backdrop, ImageType.Primary]),
                File.Type == FileType.Video  # 只修复当前类型为 Video 的
            )
        )

        records = result.all()
        print(f"找到 {len(records)} 个需要修复的文件记录")
        print()

        if not records:
            print("没有需要修复的记录")
            return

        # 2. 显示需要修复的记录
        for file_link, file in records:
            print(f"  文件ID: {file.Id}")
            print(f"  路径: {file.Path}")
            print(f"  当前类型: {file.Type}")
            print(f"  图片类型: {file_link.ImageType}")
            print(f"  关联媒体项ID: {file_link.ItemId}")
            print()

        # 3. 执行修复
        fixed_count = 0
        for file_link, file in records:
            await db.execute(
                update(File)
                .where(File.Id == file.Id)
                .values(Type=FileType.Image)
            )
            fixed_count += 1

        # 4. 提交事务
        await db.commit()

        print(f"✅ 成功修复 {fixed_count} 个文件记录")
        print()

        # 5. 验证修复结果
        result = await db.execute(
            select(File, FileLink)
            .join(FileLink, FileLink.FileId == File.Id)
            .where(
                FileLink.ImageType.in_([ImageType.Backdrop, ImageType.Primary]),
                File.Type == FileType.Video
            )
        )

        remaining = result.all()
        if remaining:
            print(f"⚠️ 还有 {len(remaining)} 个记录未修复")
        else:
            print("✅ 所有记录已正确修复")


if __name__ == "__main__":
    asyncio.run(fix_file_types())
