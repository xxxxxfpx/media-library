"""
使用 SQL 一次性修复文件类型
将 ImageType 为 Backdrop 或 Primary 的文件类型从 Video 改为 Image
"""

import asyncio
from database import AsyncSessionLocal
from sqlalchemy import text


async def fix_file_types_sql():
    """使用 SQL 批量修复文件类型"""
    async with AsyncSessionLocal() as db:
        print("开始批量修复文件类型...")
        print()

        # 1. 先查询需要修复的记录数
        count_result = await db.execute(text("""
            SELECT COUNT(*) as count
            FROM Files f
            JOIN FileLinks fl ON fl."FileId" = f."Id"
            WHERE fl."ImageType" IN ('Backdrop', 'Primary')
            AND f."Type" = 'Video'
        """))

        count = count_result.scalar()
        print(f"找到 {count} 个需要修复的文件记录")
        print()

        if count == 0:
            print("没有需要修复的记录")
            return

        # 2. 执行批量更新
        result = await db.execute(text("""
            UPDATE Files
            SET "Type" = 'Image',
                "UpdatedAt" = datetime('now')
            WHERE "Id" IN (
                SELECT f."Id"
                FROM Files f
                JOIN FileLinks fl ON fl."FileId" = f."Id"
                WHERE fl."ImageType" IN ('Backdrop', 'Primary')
                AND f."Type" = 'Video'
            )
        """))

        await db.commit()

        print(f"✅ 成功修复 {result.rowcount} 个文件记录")
        print()

        # 3. 验证修复结果
        verify_result = await db.execute(text("""
            SELECT COUNT(*) as count
            FROM Files f
            JOIN FileLinks fl ON fl."FileId" = f."Id"
            WHERE fl."ImageType" IN ('Backdrop', 'Primary')
            AND f."Type" = 'Video'
        """))

        remaining = verify_result.scalar()
        if remaining:
            print(f"⚠️ 还有 {remaining} 个记录未修复")
        else:
            print("✅ 所有记录已正确修复")


if __name__ == "__main__":
    asyncio.run(fix_file_types_sql())
