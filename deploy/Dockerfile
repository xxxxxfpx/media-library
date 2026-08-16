# 后端生产镜像
FROM python:3.12-slim AS backend

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    CONFIG_PATH=/app/config/local.yaml \
    SECRETS_PATH=/app/secrets/config.yaml

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app
COPY database ./database
COPY config ./config
COPY config.py run.py ./
COPY docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

# 运行时目录（数据库、缓存、日志）
RUN mkdir -p data/database data/log data/cache/file_url secrets

EXPOSE 8000

ENTRYPOINT ["/usr/local/bin/docker-entrypoint.sh"]
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
