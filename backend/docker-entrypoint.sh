#!/bin/sh
# 后端容器入口脚本
# - 若已挂载 secrets/config.yaml 则直接使用
# - 否则根据环境变量生成 secrets/config.yaml（避免启动守卫因 secret_key 为空拒绝启动）
set -e

SECRETS_FILE="${SECRETS_PATH:-/app/secrets/config.yaml}"

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
    echo "[entrypoint] 已生成 ${SECRETS_FILE}（secret_key=${APP_SECRET_KEY:+set}）"
fi

exec "$@"
