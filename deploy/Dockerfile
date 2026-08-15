# 后端生产镜像
FROM python:3.12-slim AS backend

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app
COPY database ./database
COPY config ./config
COPY secrets/config.example.yaml ./secrets/config.example.yaml
COPY config.py run.py ./

# 运行时目录（数据库、缓存、日志）
RUN mkdir -p data/database data/log data/cache/file_url

EXPOSE 8000

# 默认使用无敏感信息的默认配置；生产环境应挂载 config/local.yaml 或注入 CONFIG_PATH
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
