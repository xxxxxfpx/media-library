#!/bin/sh
# 后端容器入口脚本
# - 若已挂载 secrets/config.yaml 则直接使用
# - 否则根据环境变量生成 secrets/config.yaml（避免启动守卫因 secret_key 为空拒绝启动）
# - 若 APP_SECRET_KEY / APP_ADMIN_PASSWORD 未设置，则自动生成随机值并持久化
# - 启动前自动执行数据库迁移和表结构修复
set -e

SECRETS_FILE="${SECRETS_PATH:-/app/secrets/config.yaml}"

# ── 0. 确保运行时数据目录存在 ──
# bind mount 会覆盖镜像内 Dockerfile 创建的目录，需在启动时重建
mkdir -p /app/data/database /app/data/log /app/data/cache/file_url /app/secrets

# ── 1. 兜底生成随机密钥（仅当未显式设置时） ──
if [ -z "${APP_SECRET_KEY:-}" ]; then
    APP_SECRET_KEY="$(head -c 48 /dev/urandom | base64 | tr -d '\n')"
    echo "[entrypoint] 未设置 APP_SECRET_KEY，已自动生成随机密钥（长度=${#APP_SECRET_KEY}）"
fi

if [ -z "${APP_ADMIN_PASSWORD:-}" ]; then
    # 随机生成 16 位密码并打印到日志，方便首次部署后查看
    APP_ADMIN_PASSWORD="$(head -c 16 /dev/urandom | base64 | tr -dc 'A-Za-z0-9' | head -c 16)"
    echo "[entrypoint] 未设置 APP_ADMIN_PASSWORD，已自动生成随机密码：${APP_ADMIN_PASSWORD}"
    echo "[entrypoint] ⚠️ 请妥善保管此密码；如需重置，下次启动前重新设置 APP_ADMIN_PASSWORD"
fi

# ── 2. 生成 secrets/config.yaml（若已存在则跳过） ──
if [ ! -f "$SECRETS_FILE" ]; then
    echo "[entrypoint] ${SECRETS_FILE} 不存在，根据环境变量生成…"
    mkdir -p "$(dirname "$SECRETS_FILE")"
    cat > "$SECRETS_FILE" <<YAML
app:
  secret_key: "${APP_SECRET_KEY}"
  admin:
    username: "${APP_ADMIN_USERNAME:-admin}"
    password: "${APP_ADMIN_PASSWORD}"
cloud_auth:
  username: "${CLOUD_USERNAME:-}"
  password: "${CLOUD_PASSWORD:-}"
  prefix: "${CLOUD_PREFIX:-/}"
YAML
    echo "[entrypoint] 已生成 ${SECRETS_FILE}（secret_key=set, admin_password=set）"
else
    echo "[entrypoint] 已存在 ${SECRETS_FILE}，沿用现有配置"
fi

# ── 3. 直接用 SQL 修复旧数据库缺失的列（兼容 alembic 版本不匹配的情况） ──
DB_PATH="/app/data/database/media.db"
if [ -f "$DB_PATH" ]; then
    echo "[entrypoint] 检测到现有数据库，检查并修复缺失的列..."
    
    python -c "
import sqlite3
conn = sqlite3.connect('$DB_PATH')
cursor = conn.cursor()

# 定义需要检查的表和列
required_columns = {
    'CollectionSources': {
        'SortOrder': \"TEXT DEFAULT 'time'\",
        'LastMaxItemId': 'INTEGER DEFAULT 0',
    },
    'MediaItems': {
        'OriginalLanguage': 'TEXT',
        'BirthPlace': 'TEXT',
    },
}

for table, columns in required_columns.items():
    cursor.execute(\"SELECT name FROM sqlite_master WHERE type='table' AND name='\" + table + \"'\")
    if not cursor.fetchone():
        print(f'[entrypoint] {table} 表不存在，跳过')
        continue
    
    cursor.execute(f'PRAGMA table_info({table})')
    existing_columns = [col[1] for col in cursor.fetchall()]
    
    for col_name, col_def in columns.items():
        if col_name not in existing_columns:
            print(f'[entrypoint] 为 {table} 添加 {col_name} 列...')
            cursor.execute(f'ALTER TABLE {table} ADD COLUMN {col_name} {col_def}')
            if col_def.startswith('TEXT DEFAULT'):
                default_val = col_def.split(\"'\")[1] if \"'\" in col_def else ''
                if default_val:
                    cursor.execute(f\"UPDATE {table} SET {col_name} = '{default_val}' WHERE {col_name} IS NULL\")
            elif 'DEFAULT' in col_def:
                default_val = col_def.split('DEFAULT')[1].strip()
                cursor.execute(f'UPDATE {table} SET {col_name} = {default_val} WHERE {col_name} IS NULL')
    
    print(f'[entrypoint] {table} 表检查完成')

conn.commit()
conn.close()
" 2>&1 || echo "[entrypoint] ⚠️ 数据库修复脚本执行失败"
fi

# ── 4. 执行 Alembic 数据库迁移（如果 alembic_version 匹配） ──
echo "[entrypoint] 尝试执行数据库迁移..."
cd /app
if python -m alembic -c database/alembic.ini upgrade head 2>/dev/null; then
    echo "[entrypoint] 数据库迁移完成"
else
    echo "[entrypoint] ⚠️ Alembic 迁移失败（可能是版本不匹配），继续启动..."
fi

exec "$@"
