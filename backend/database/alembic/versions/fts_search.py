"""fts_search

Revision ID: fts_search
Revises: db_optimization_indexes_v2
Create Date: 2026-08-16 00:00:00.000000

搜索性能优化：
- SQLite：FTS5 trigram 虚拟表（media_item_fts，外部内容表）+ 同步触发器
  （trigram 分词器支持 >=3 字符的子串匹配，命中 Name/Overview/Tagline；
   短查询由服务层回退 LIKE）
- PostgreSQL：pg_trgm GIN 索引，使 ILIKE '%x%' 走索引（含 Aliases.Name）
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from database.fts_ddl import FTS5_CREATE_SQL, FTS5_DROP_SQL


# revision identifiers, used by Alembic.
revision: str = 'fts_search'
down_revision: Union[str, Sequence[str], None] = 'db_optimization_indexes_v2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def _create_sqlite_fts(conn) -> None:
    """创建 FTS5 外部内容虚拟表与同步触发器（幂等，DDL 与 database/core.py 共用单一来源）"""
    for statement in FTS5_CREATE_SQL:
        conn.execute(sa.text(statement))


def _create_pg_trgm(conn) -> None:
    conn.execute(sa.text("CREATE EXTENSION IF NOT EXISTS pg_trgm"))
    conn.execute(sa.text(
        "CREATE INDEX IF NOT EXISTS idx_media_items_name_trgm ON MediaItems USING gin (Name gin_trgm_ops)"
    ))
    conn.execute(sa.text(
        "CREATE INDEX IF NOT EXISTS idx_media_items_overview_trgm ON MediaItems USING gin (Overview gin_trgm_ops)"
    ))
    conn.execute(sa.text(
        "CREATE INDEX IF NOT EXISTS idx_media_items_tagline_trgm ON MediaItems USING gin (Tagline gin_trgm_ops)"
    ))
    conn.execute(sa.text(
        "CREATE INDEX IF NOT EXISTS idx_aliases_name_trgm ON Aliases USING gin (Name gin_trgm_ops)"
    ))


def upgrade() -> None:
    bind = op.get_bind()
    if bind.dialect.name == "sqlite":
        _create_sqlite_fts(bind)
    elif bind.dialect.name == "postgresql":
        _create_pg_trgm(bind)


def downgrade() -> None:
    bind = op.get_bind()
    if bind.dialect.name == "sqlite":
        for statement in FTS5_DROP_SQL:
            bind.execute(sa.text(statement))
    elif bind.dialect.name == "postgresql":
        bind.execute(sa.text("DROP INDEX IF EXISTS idx_aliases_name_trgm"))
        bind.execute(sa.text("DROP INDEX IF EXISTS idx_media_items_tagline_trgm"))
        bind.execute(sa.text("DROP INDEX IF EXISTS idx_media_items_overview_trgm"))
        bind.execute(sa.text("DROP INDEX IF EXISTS idx_media_items_name_trgm"))
