"""
FTS5 虚拟表与同步触发器 DDL 定义（单一来源）
==========================================

database/core.py 的运行时建表（init_db，供未跑迁移的 SQLite 环境）与
alembic 迁移 fts_search 共用同一套 DDL，避免两处维护造成漂移。

用法：
    async 连接（core.py）：for stmt in FTS5_CREATE_SQL: await conn.execute(text(stmt))
    同步连接（alembic）：for stmt in FTS5_CREATE_SQL: conn.execute(sa.text(stmt))
"""

FTS5_CREATE_SQL = [
    # 外部内容表：Name/Overview/Tagline 走 trigram 分词（>=3 字符子串匹配）
    """CREATE VIRTUAL TABLE IF NOT EXISTS media_item_fts USING fts5(
        Name, Overview, Tagline,
        content='MediaItems', content_rowid='Id',
        tokenize='trigram'
    )""",
    # 同步触发器：INSERT
    """CREATE TRIGGER IF NOT EXISTS media_item_fts_ai AFTER INSERT ON MediaItems BEGIN
        INSERT INTO media_item_fts(rowid, Name, Overview, Tagline)
        VALUES (new.Id, new.Name, new.Overview, new.Tagline);
    END""",
    # 同步触发器：DELETE
    """CREATE TRIGGER IF NOT EXISTS media_item_fts_ad AFTER DELETE ON MediaItems BEGIN
        INSERT INTO media_item_fts(media_item_fts, rowid, Name, Overview, Tagline)
        VALUES ('delete', old.Id, old.Name, old.Overview, old.Tagline);
    END""",
    # 同步触发器：UPDATE（先删旧行再插新行）
    """CREATE TRIGGER IF NOT EXISTS media_item_fts_au AFTER UPDATE ON MediaItems BEGIN
        INSERT INTO media_item_fts(media_item_fts, rowid, Name, Overview, Tagline)
        VALUES ('delete', old.Id, old.Name, old.Overview, old.Tagline);
        INSERT INTO media_item_fts(rowid, Name, Overview, Tagline)
        VALUES (new.Id, new.Name, new.Overview, new.Tagline);
    END""",
    # 重建索引：从内容表回填所有行（幂等，重复执行无副作用）
    "INSERT INTO media_item_fts(media_item_fts) VALUES('rebuild')",
]

FTS5_DROP_SQL = [
    "DROP TRIGGER IF EXISTS media_item_fts_ai",
    "DROP TRIGGER IF EXISTS media_item_fts_ad",
    "DROP TRIGGER IF EXISTS media_item_fts_au",
    "DROP TABLE IF EXISTS media_item_fts",
]
