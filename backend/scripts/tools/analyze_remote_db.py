"""
远程 PostgreSQL 数据库结构分析脚本
"""
import asyncio
import asyncpg
import json
from datetime import datetime
from config import get_remote_db_config

# 远程数据库连接信息
REMOTE_DB_CONFIG = get_remote_db_config()


async def analyze_database():
    """分析远程数据库结构"""
    print("=" * 80)
    print("远程 PostgreSQL 数据库结构分析")
    print(f"主机: {REMOTE_DB_CONFIG['host']}:{REMOTE_DB_CONFIG['port']}")
    print(f"数据库: {REMOTE_DB_CONFIG['database']}")
    print("=" * 80)
    
    try:
        conn = await asyncpg.connect(**REMOTE_DB_CONFIG)
        print("✅ 数据库连接成功\n")
        
        # 1. 获取所有表
        tables_query = """
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public' 
        ORDER BY table_name
        """
        tables = await conn.fetch(tables_query)
        
        print(f"📊 发现 {len(tables)} 个表:")
        for table in tables:
            print(f"   - {table['table_name']}")
        print()
        
        # 2. 分析每个表的结构
        schema_info = {}
        
        for table in tables:
            table_name = table['table_name']
            print(f"\n🔍 分析表: {table_name}")
            print("-" * 60)
            
            # 获取列信息
            columns_query = """
            SELECT 
                column_name,
                data_type,
                is_nullable,
                column_default,
                character_maximum_length,
                numeric_precision,
                numeric_scale
            FROM information_schema.columns
            WHERE table_schema = 'public' AND table_name = $1
            ORDER BY ordinal_position
            """
            columns = await conn.fetch(columns_query, table_name)
            
            # 获取主键
            pk_query = """
            SELECT kcu.column_name
            FROM information_schema.table_constraints tc
            JOIN information_schema.key_column_usage kcu 
                ON tc.constraint_name = kcu.constraint_name
            WHERE tc.constraint_type = 'PRIMARY KEY' 
                AND tc.table_name = $1
            """
            pk_columns = await conn.fetch(pk_query, table_name)
            pk_set = {row['column_name'] for row in pk_columns}
            
            # 获取外键
            fk_query = """
            SELECT
                kcu.column_name,
                ccu.table_name AS foreign_table_name,
                ccu.column_name AS foreign_column_name
            FROM information_schema.table_constraints tc
            JOIN information_schema.key_column_usage kcu
                ON tc.constraint_name = kcu.constraint_name
            JOIN information_schema.constraint_column_usage ccu
                ON ccu.constraint_name = tc.constraint_name
            WHERE tc.constraint_type = 'FOREIGN KEY' 
                AND tc.table_name = $1
            """
            fk_columns = await conn.fetch(fk_query, table_name)
            
            # 获取索引
            index_query = """
            SELECT indexname, indexdef
            FROM pg_indexes
            WHERE tablename = $1 AND schemaname = 'public'
            """
            indexes = await conn.fetch(index_query, table_name)
            
            # 获取记录数
            count_query = f'SELECT COUNT(*) FROM "{table_name}"'
            try:
                count_result = await conn.fetchval(count_query)
            except:
                count_result = 0
            
            table_info = {
                'columns': [],
                'primary_keys': list(pk_set),
                'foreign_keys': [dict(row) for row in fk_columns],
                'indexes': [dict(row) for row in indexes],
                'record_count': count_result
            }
            
            for col in columns:
                col_info = {
                    'name': col['column_name'],
                    'type': col['data_type'],
                    'nullable': col['is_nullable'] == 'YES',
                    'default': col['column_default'],
                    'is_primary': col['column_name'] in pk_set
                }
                if col['character_maximum_length']:
                    col_info['max_length'] = col['character_maximum_length']
                table_info['columns'].append(col_info)
                print(f"   {'🔑' if col['column_name'] in pk_set else '  '} {col['column_name']:30} {col['data_type']:<20} {'NULL' if col['is_nullable'] == 'YES' else 'NOT NULL'}")
            
            print(f"\n   📈 记录数: {count_result}")
            if pk_columns:
                print(f"   🔐 主键: {', '.join(pk_set)}")
            if fk_columns:
                print(f"   🔗 外键:")
                for fk in fk_columns:
                    print(f"      {fk['column_name']} -> {fk['foreign_table_name']}.{fk['foreign_column_name']}")
            
            schema_info[table_name] = table_info
        
        # 3. 保存分析结果
        output_file = 'remote_db_schema.json'
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(schema_info, f, ensure_ascii=False, indent=2)
        print(f"\n\n✅ 分析结果已保存到: {output_file}")
        
        await conn.close()
        return schema_info
        
    except Exception as e:
        print(f"❌ 错误: {e}")
        return None


async def compare_with_local_model():
    """与当前项目模型对比"""
    print("\n" + "=" * 80)
    print("与当前项目模型对比")
    print("=" * 80)
    
    # 当前项目的模型（从代码中提取）
    local_models = {
        'Users': ['Id', 'Name', 'PasswordHash', 'Salt', 'Email', 'IsAdmin', 'IsActive', 'Setting', 'CreatedAt', 'UpdatedAt'],
        'UserData': ['Id', 'UserId', 'ItemId', 'IsFavorite', 'PlaybackPositionTicks', 'PlayCount', 'IsPlayed', 'Rating', 'LastPlayedAt', 'FavoritedAt', 'CreatedAt', 'UpdatedAt'],
        'UserItemShares': ['Id', 'UserId', 'ItemId', 'ShareToken', 'ExpiresAt', 'CreatedAt'],
        'MediaItems': ['Id', 'Name', 'SortName', 'OriginalTitle', 'Overview', 'Tagline', 'Type', 'ProductionYear', 'PremiereDate', 'EndDate', 'RunTimeTicks', 'OfficialRating', 'CommunityRating', 'CriticRating', 'IsDeleted', 'DateCreated', 'DateModified', 'CreatedAt', 'UpdatedAt'],
        'ItemLinks': ['Id', 'ItemId', 'LinkedItemId', 'Type', 'PeopleType', 'PeopleRole', 'CreatedAt', 'UpdatedAt'],
        'Files': ['Id', 'Etag', 'Size', 'Name', 'SortName', 'Path', 'CloudId', 'Type', 'FFmpeg', 'CreatedAt', 'UpdatedAt'],
        'FileLinks': ['Id', 'ItemId', 'FileId', 'ImageType', 'ImageIndex', 'CreatedAt', 'UpdatedAt'],
        'Aliases': ['Id', 'ItemId', 'Name', 'Source', 'CreatedAt', 'UpdatedAt']
    }
    
    for table, columns in local_models.items():
        print(f"\n📋 {table}:")
        print(f"   本地列: {', '.join(columns)}")
    
    return local_models


async def main():
    print("\n🔍 开始分析远程数据库...\n")
    
    # 分析远程数据库
    remote_schema = await analyze_database()
    
    if remote_schema:
        # 对比本地模型
        local_models = await compare_with_local_model()
        
        # 生成迁移分析报告
        print("\n" + "=" * 80)
        print("迁移分析摘要")
        print("=" * 80)
        
        remote_tables = set(remote_schema.keys())
        local_tables = set(local_models.keys())
        
        print(f"\n📊 表对比:")
        print(f"   远程数据库表: {len(remote_tables)} 个")
        print(f"   本地项目表: {len(local_tables)} 个")
        print(f"   共同表: {len(remote_tables & local_tables)} 个")
        print(f"   仅远程存在: {remote_tables - local_tables}")
        print(f"   仅本地存在: {local_tables - remote_tables}")


if __name__ == '__main__':
    asyncio.run(main())
