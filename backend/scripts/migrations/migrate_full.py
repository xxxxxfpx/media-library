"""
全量数据迁移框架

功能：
- 从远程 PostgreSQL 数据库迁移数据到本地 SQLite 数据库
- 支持 ID 映射管理、事务处理、批量处理
- 提供断点续传、详细日志记录、时区转换功能

作者：Assistant
创建日期：2026-04-25
"""

import asyncio
import logging
from datetime import datetime, timezone, timedelta
from typing import Any, Dict, List, Optional, Tuple
from contextlib import asynccontextmanager
import json
import os

import asyncpg
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy import text

# ============================================================================
# 配置模块
# ============================================================================

class Config:
    """数据库连接配置"""
    
    # 远程 PostgreSQL 配置
    POSTGRES_HOST = os.environ.get('REMOTE_DB_HOST', '')
    POSTGRES_PORT = 5432
    POSTGRES_DATABASE = "emby"
    POSTGRES_USER = os.environ.get('REMOTE_DB_USER', '')
    POSTGRES_PASSWORD = os.environ.get('REMOTE_DB_PASSWORD', '')
    
    # 本地 SQLite 配置
    SQLITE_DATABASE = "data/database/media.db"
    
    # 批量处理配置
    BATCH_SIZE = 500  # 每批处理 500 条记录
    
    # 时区配置 (UTC+8)
    TIMEZONE_OFFSET = timedelta(hours=8)
    
    # 断点续传文件
    CHECKPOINT_FILE = "migrate_checkpoint.json"
    
    @classmethod
    def get_postgres_uri(cls) -> str:
        """获取 PostgreSQL 连接 URI"""
        return (
            f"postgresql://{cls.POSTGRES_USER}:{cls.POSTGRES_PASSWORD}"
            f"@{cls.POSTGRES_HOST}:{cls.POSTGRES_PORT}/{cls.POSTGRES_DATABASE}"
        )
    
    @classmethod
    def get_sqlite_uri(cls) -> str:
        """获取 SQLite 连接 URI"""
        return f"sqlite+aiosqlite:///{cls.SQLITE_DATABASE}"


# ============================================================================
# 日志模块
# ============================================================================

def setup_logging() -> logging.Logger:
    """配置日志系统"""
    logger = logging.getLogger("DataMigration")
    logger.setLevel(logging.INFO)
    
    # 控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    
    # 文件处理器
    file_handler = logging.FileHandler("migration.log", encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    
    # 格式化器
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)
    
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    
    return logger


logger = setup_logging()


# ============================================================================
# 时间戳转换工具
# ============================================================================

class TimestampConverter:
    """时间戳转换工具 (UTC+8)"""
    
    @staticmethod
    def convert_utc_to_utc8(timestamp: datetime) -> datetime:
        """将 UTC 时间转换为 UTC+8 时间"""
        if timestamp.tzinfo is None:
            timestamp = timestamp.replace(tzinfo=timezone.utc)
        return timestamp.astimezone(timezone(Config.TIMEZONE_OFFSET))
    
    @staticmethod
    def convert_timestamp(
        timestamp: Optional[datetime],
        from_utc: bool = True
    ) -> Optional[datetime]:
        """转换时间戳"""
        if timestamp is None:
            return None
        if from_utc:
            return TimestampConverter.convert_utc_to_utc8(timestamp)
        return timestamp


# ============================================================================
# ID 映射管理
# ============================================================================

class IDMapper:
    """ID 映射管理器 - 管理远程 ID 到本地 ID 的映射关系"""
    
    def __init__(self):
        self._mapping: Dict[str, Dict[int, int]] = {}
        self._reverse_mapping: Dict[str, Dict[int, int]] = {}
    
    def add_mapping(
        self,
        table_name: str,
        remote_id: int,
        local_id: int
    ) -> None:
        """添加 ID 映射"""
        if table_name not in self._mapping:
            self._mapping[table_name] = {}
            self._reverse_mapping[table_name] = {}
        
        self._mapping[table_name][remote_id] = local_id
        self._reverse_mapping[table_name][local_id] = remote_id
    
    def get_local_id(
        self,
        table_name: str,
        remote_id: int
    ) -> Optional[int]:
        """根据远程 ID 获取本地 ID"""
        return self._mapping.get(table_name, {}).get(remote_id)
    
    def get_remote_id(
        self,
        table_name: str,
        local_id: int
    ) -> Optional[int]:
        """根据本地 ID 获取远程 ID"""
        return self._reverse_mapping.get(table_name, {}).get(local_id)
    
    def has_mapping(
        self,
        table_name: str,
        remote_id: int
    ) -> bool:
        """检查是否存在映射"""
        return table_name in self._mapping and remote_id in self._mapping[table_name]
    
    def get_mapping_count(self, table_name: str) -> int:
        """获取表的映射数量"""
        return len(self._mapping.get(table_name, {}))
    
    def export_mapping(self) -> Dict[str, Dict[str, int]]:
        """导出映射为字典"""
        return {
            table: {str(k): v for k, v in mapping.items()}
            for table, mapping in self._mapping.items()
        }
    
    def import_mapping(self, data: Dict[str, Dict[str, int]]) -> None:
        """从字典导入映射"""
        for table, mapping in data.items():
            self._mapping[table] = {}
            self._reverse_mapping[table] = {}
            for remote_id, local_id in mapping.items():
                remote_id_int = int(remote_id)
                self._mapping[table][remote_id_int] = local_id
                self._reverse_mapping[table][local_id] = remote_id_int


# ============================================================================
# 断点续传管理
# ============================================================================

class CheckpointManager:
    """断点续传管理器 - 记录迁移进度"""
    
    def __init__(self, checkpoint_file: str):
        self.checkpoint_file = checkpoint_file
        self._data: Dict[str, Any] = {
            "migrated_ids": {},
            "last_updated": None,
            "statistics": {
                "total_success": 0,
                "total_failed": 0,
                "tables": {}
            }
        }
        self._load_checkpoint()
    
    def _load_checkpoint(self) -> None:
        """加载断点文件"""
        if os.path.exists(self.checkpoint_file):
            try:
                with open(self.checkpoint_file, "r", encoding="utf-8") as f:
                    self._data = json.load(f)
                logger.info(f"已加载断点文件：{self.checkpoint_file}")
            except Exception as e:
                logger.warning(f"加载断点文件失败：{e}，将从头开始")
                self._data = {
                    "migrated_ids": {},
                    "last_updated": None,
                    "statistics": {
                        "total_success": 0,
                        "total_failed": 0,
                        "tables": {}
                    }
                }
    
    def save_checkpoint(self) -> None:
        """保存断点"""
        self._data["last_updated"] = datetime.now().isoformat()
        try:
            with open(self.checkpoint_file, "w", encoding="utf-8") as f:
                json.dump(self._data, f, ensure_ascii=False, indent=2)
            logger.debug(f"已保存断点文件：{self.checkpoint_file}")
        except Exception as e:
            logger.error(f"保存断点文件失败：{e}")
    
    def is_migrated(self, table_name: str, remote_id: int) -> bool:
        """检查记录是否已迁移"""
        table_key = f"table:{table_name}"
        return table_key in self._data["migrated_ids"] and \
               str(remote_id) in self._data["migrated_ids"][table_key]
    
    def mark_migrated(self, table_name: str, remote_id: int, local_id: int) -> None:
        """标记记录已迁移"""
        table_key = f"table:{table_name}"
        if table_key not in self._data["migrated_ids"]:
            self._data["migrated_ids"][table_key] = {}
        self._data["migrated_ids"][table_key][str(remote_id)] = local_id
        self._data["statistics"]["total_success"] += 1
        
        if table_name not in self._data["statistics"]["tables"]:
            self._data["statistics"]["tables"][table_name] = {
                "success": 0,
                "failed": 0
            }
        self._data["statistics"]["tables"][table_name]["success"] += 1
    
    def mark_failed(self, table_name: str, remote_id: int, error: str) -> None:
        """标记记录迁移失败"""
        self._data["statistics"]["total_failed"] += 1
        
        if table_name not in self._data["statistics"]["tables"]:
            self._data["statistics"]["tables"][table_name] = {
                "success": 0,
                "failed": 0
            }
        self._data["statistics"]["tables"][table_name]["failed"] += 1
        
        logger.error(f"迁移失败 - 表：{table_name}, ID: {remote_id}, 错误：{error}")
    
    def get_migrated_ids(self, table_name: str) -> Dict[int, int]:
        """获取表已迁移的 ID 映射"""
        table_key = f"table:{table_name}"
        migrated = self._data["migrated_ids"].get(table_key, {})
        return {int(k): v for k, v in migrated.items()}
    
    def get_statistics(self) -> Dict[str, Any]:
        """获取统计信息"""
        return self._data["statistics"]


# ============================================================================
# 数据库连接管理
# ============================================================================

class DatabaseManager:
    """数据库连接管理器"""
    
    def __init__(self, config: Config):
        self.config = config
        self._postgres_pool: Optional[asyncpg.Pool] = None
        self._sqlite_engine: Optional[Any] = None
        self._sqlite_session_factory: Optional[async_sessionmaker] = None
    
    async def init_postgres(self) -> None:
        """初始化 PostgreSQL 连接池"""
        try:
            self._postgres_pool = await asyncpg.create_pool(
                host=self.config.POSTGRES_HOST,
                port=self.config.POSTGRES_PORT,
                database=self.config.POSTGRES_DATABASE,
                user=self.config.POSTGRES_USER,
                password=self.config.POSTGRES_PASSWORD,
                min_size=2,
                max_size=10,
                command_timeout=60
            )
            logger.info("PostgreSQL 连接池初始化成功")
        except Exception as e:
            logger.error(f"PostgreSQL 连接池初始化失败：{e}")
            raise
    
    async def init_sqlite(self) -> None:
        """初始化 SQLite 引擎"""
        try:
            self._sqlite_engine = create_async_engine(
                self.config.get_sqlite_uri(),
                echo=False,
                pool_pre_ping=True
            )
            self._sqlite_session_factory = async_sessionmaker(
                self._sqlite_engine,
                class_=AsyncSession,
                expire_on_commit=False
            )
            logger.info("SQLite 引擎初始化成功")
        except Exception as e:
            logger.error(f"SQLite 引擎初始化失败：{e}")
            raise
    
    @asynccontextmanager
    async def postgres_connection(self):
        """获取 PostgreSQL 连接上下文管理器"""
        if self._postgres_pool is None:
            raise RuntimeError("PostgreSQL 连接池未初始化")
        async with self._postgres_pool.acquire() as connection:
            yield connection
    
    @asynccontextmanager
    async def sqlite_session(self) -> AsyncSession:
        """获取 SQLite 会话上下文管理器"""
        if self._sqlite_session_factory is None:
            raise RuntimeError("SQLite 会话工厂未初始化")
        async with self._sqlite_session_factory() as session:
            yield session
    
    async def close(self) -> None:
        """关闭数据库连接"""
        if self._postgres_pool:
            await self._postgres_pool.close()
            logger.info("PostgreSQL 连接池已关闭")
        
        if self._sqlite_engine:
            await self._sqlite_engine.dispose()
            logger.info("SQLite 引擎已关闭")


# ============================================================================
# 迁移统计
# ============================================================================

class MigrationStats:
    """迁移统计信息"""
    
    def __init__(self):
        self.total_success = 0
        self.total_failed = 0
        self.tables: Dict[str, Dict[str, int]] = {}
        self.start_time: Optional[datetime] = None
        self.end_time: Optional[datetime] = None
    
    def start(self) -> None:
        """开始统计"""
        self.start_time = datetime.now()
    
    def stop(self) -> None:
        """结束统计"""
        self.end_time = datetime.now()
    
    def add_table(self, table_name: str) -> None:
        """添加表统计"""
        if table_name not in self.tables:
            self.tables[table_name] = {"success": 0, "failed": 0}
    
    def record_success(self, table_name: str, count: int = 1) -> None:
        """记录成功"""
        self.total_success += count
        if table_name in self.tables:
            self.tables[table_name]["success"] += count
    
    def record_failed(self, table_name: str, count: int = 1) -> None:
        """记录失败"""
        self.total_failed += count
        if table_name in self.tables:
            self.tables[table_name]["failed"] += count
    
    def get_duration(self) -> str:
        """获取迁移耗时"""
        if self.start_time and self.end_time:
            duration = self.end_time - self.start_time
            return str(duration)
        return "N/A"
    
    def summary(self) -> str:
        """获取统计摘要"""
        lines = [
            "=" * 60,
            "迁移统计摘要",
            "=" * 60,
            f"开始时间：{self.start_time}",
            f"结束时间：{self.end_time}",
            f"总耗时：{self.get_duration()}",
            f"成功记录数：{self.total_success}",
            f"失败记录数：{self.total_failed}",
            f"成功率：{self.total_success / (self.total_success + self.total_failed) * 100:.2f}%"
            if (self.total_success + self.total_failed) > 0 else "成功率：N/A",
            "-" * 60,
            "表明细:"
        ]
        
        for table, stats in self.tables.items():
            lines.append(
                f"  {table}: 成功={stats['success']}, 失败={stats['failed']}"
            )
        
        lines.append("=" * 60)
        return "\n".join(lines)


# ============================================================================
# 迁移框架主类
# ============================================================================

class DataMigrationFramework:
    """数据迁移框架主类"""
    
    def __init__(self):
        self.config = Config()
        self.db_manager = DatabaseManager(self.config)
        self.id_mapper = IDMapper()
        self.checkpoint = CheckpointManager(self.config.CHECKPOINT_FILE)
        self.stats = MigrationStats()
    
    async def initialize(self) -> None:
        """初始化迁移框架"""
        logger.info("正在初始化迁移框架...")
        await self.db_manager.init_postgres()
        await self.db_manager.init_sqlite()
        logger.info("迁移框架初始化完成")
    
    async def cleanup(self) -> None:
        """清理资源"""
        await self.db_manager.close()
        self.checkpoint.save_checkpoint()
        logger.info(self.stats.summary())
    
    async def migrate_table(
        self,
        table_name: str,
        fetch_func,
        process_func,
        columns: Optional[List[str]] = None
    ) -> None:
        """
        迁移单个表的通用方法
        
        参数:
            table_name: 表名
            fetch_func: 获取数据的异步函数 (connection, batch_size, offset) -> List[Dict]
            process_func: 处理数据的异步函数 (session, record, mapper) -> local_id
            columns: 需要迁移的列名
        """
        logger.info(f"开始迁移表：{table_name}")
        self.stats.add_table(table_name)
        
        offset = 0
        batch_size = self.config.BATCH_SIZE
        total_processed = 0
        
        while True:
            try:
                async with self.db_manager.postgres_connection() as conn:
                    records = await fetch_func(conn, batch_size, offset)
                    
                    if not records:
                        logger.info(f"表 {table_name} 迁移完成，共处理 {total_processed} 条记录")
                        break
                    
                    async with self.db_manager.sqlite_session() as session:
                        async with session.begin():
                            for record in records:
                                try:
                                    remote_id = record.get("id")
                                    
                                    if self.checkpoint.is_migrated(table_name, remote_id):
                                        logger.debug(
                                            f"记录已迁移，跳过 - 表：{table_name}, ID: {remote_id}"
                                        )
                                        continue
                                    
                                    local_id = await process_func(
                                        session, record, self.id_mapper
                                    )
                                    
                                    if local_id:
                                        self.id_mapper.add_mapping(
                                            table_name, remote_id, local_id
                                        )
                                        self.checkpoint.mark_migrated(
                                            table_name, remote_id, local_id
                                        )
                                        self.stats.record_success(table_name)
                                    
                                    total_processed += 1
                                    
                                except Exception as e:
                                    self.stats.record_failed(table_name)
                                    self.checkpoint.mark_failed(
                                        table_name,
                                        record.get("id", "unknown"),
                                        str(e)
                                    )
                                    logger.exception(
                                        f"处理记录失败 - 表：{table_name}, ID: {record.get('id')}"
                                    )
                    
                    offset += batch_size
                    
                    if offset % (batch_size * 10) == 0:
                        self.checkpoint.save_checkpoint()
                        logger.info(f"已处理 {table_name}: {total_processed} 条记录")
                        
            except Exception as e:
                logger.exception(f"迁移表 {table_name} 时发生错误：{e}")
                raise
        
        logger.info(f"表 {table_name} 迁移完成")
    
    async def run_migration(self) -> None:
        """
        执行迁移 - 子类需要实现此方法
        
        示例:
            await self.migrate_table(
                table_name="movies",
                fetch_func=self._fetch_movies,
                process_func=self._process_movie
            )
        """
        raise NotImplementedError("子类需要实现 run_migration 方法")
    
    async def run(self) -> None:
        """运行迁移"""
        self.stats.start()
        logger.info("=" * 60)
        logger.info("开始数据迁移")
        logger.info("=" * 60)
        
        try:
            await self.initialize()
            await self.run_migration()
            logger.info("数据迁移完成")
        except Exception as e:
            logger.exception(f"迁移过程中发生错误：{e}")
            raise
        finally:
            await self.cleanup()
            self.stats.stop()


# ============================================================================
# 示例迁移实现 (供参考)
# ============================================================================

class ExampleMigration(DataMigrationFramework):
    """示例迁移实现 - 展示如何使用框架"""
    
    async def _fetch_example(
        self,
        conn: asyncpg.Connection,
        batch_size: int,
        offset: int
    ) -> List[Dict]:
        """示例：获取数据的函数"""
        query = """
            SELECT id, name, created_at, updated_at
            FROM example_table
            ORDER BY id
            LIMIT $1 OFFSET $2
        """
        rows = await conn.fetch(query, batch_size, offset)
        return [dict(row) for row in rows]
    
    async def _process_example(
        self,
        session: AsyncSession,
        record: Dict,
        mapper: IDMapper
    ) -> Optional[int]:
        """示例：处理数据的函数"""
        try:
            converted_time = TimestampConverter.convert_timestamp(
                record.get("created_at")
            )
            
            result = await session.execute(
                text("""
                    INSERT INTO example_table (name, created_at, updated_at)
                    VALUES (:name, :created_at, :updated_at)
                    RETURNING id
                """),
                {
                    "name": record.get("name"),
                    "created_at": converted_time,
                    "updated_at": TimestampConverter.convert_timestamp(
                        record.get("updated_at")
                    )
                }
            )
            
            local_id = result.scalar()
            return local_id
            
        except Exception as e:
            logger.error(f"处理示例记录失败：{e}")
            return None
    
    async def run_migration(self) -> None:
        """实现迁移逻辑"""
        await self.migrate_table(
            table_name="example_table",
            fetch_func=self._fetch_example,
            process_func=self._process_example
        )


# ============================================================================
# 主函数
# ============================================================================

async def main():
    """主函数"""
    migration = ExampleMigration()
    await migration.run()


if __name__ == "__main__":
    asyncio.run(main())
