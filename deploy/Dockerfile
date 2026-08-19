# 多阶段构建：在 Runner 上完成前端静态资源 + 后端镜像，
# 最终单镜像同时提供 FastAPI + SPA 静态文件，服务器只需 docker compose up

# ── 阶段 1：构建前端静态资源 ──
FROM node:20-alpine AS frontend-builder

WORKDIR /src/frontend

# 先拷贝依赖清单以利用 Docker 缓存
COPY frontend/package.json frontend/package-lock.json ./

RUN npm ci

COPY frontend/ ./

RUN npm run build

# ── 阶段 2：打包后端 + 前端静态资源 ──
FROM python:3.12-slim AS runtime

ARG APP_VERSION
ENV APP_VERSION=${APP_VERSION:-unknown}

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    CONFIG_PATH=/app/config/default.yaml \
    SECRETS_PATH=/app/secrets/config.yaml

WORKDIR /app

COPY backend/requirements.txt .

# 构建期使用国内 PyPI 镜像加速
ENV PIP_INDEX_URL=https://mirrors.aliyun.com/pypi/simple/
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/app ./app
COPY backend/database ./database
COPY backend/config ./config
COPY backend/config.py backend/run.py ./
COPY backend/docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

# 将前端构建产物放入静态目录，由 FastAPI 托管
COPY --from=frontend-builder /src/frontend/dist /app/static

# 运行时目录
RUN mkdir -p data/database data/log data/cache/file_url secrets

EXPOSE 8000

ENTRYPOINT ["/usr/local/bin/docker-entrypoint.sh"]
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
