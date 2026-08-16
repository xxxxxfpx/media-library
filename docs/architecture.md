# 系统架构

## 技术栈

- **后端**：Python FastAPI + SQLAlchemy 2.0 async + JWT (python-jose) + Pydantic v2
- **前端**：Vue 3 (Composition API) + Vite + Pinia + Element Plus + Axios
- **移动端**：Flutter 3.x + Riverpod + Dio + media_kit
- **数据库**：SQLite (aiosqlite，默认，WAL 模式) / PostgreSQL (asyncpg，生产可选)
- **文件存储**：123 云盘 WebDAV（文件通过 302 重定向提供）

## 目录结构

```text
media-library/
├─ backend/          # 后端（可独立部署单元）
│  ├─ app/           # FastAPI 应用（api / services / schemas）
│  ├─ database/      # SQLAlchemy 模型、引擎、Alembic 迁移
│  ├─ tests/         # pytest 测试
│  ├─ scripts/       # 数据校验/迁移/运维脚本（按职责拆分）
│  ├─ config/        # 配置文件（default/local/setting）
│  ├─ data/          # 运行时数据（数据库、缓存、日志）
│  ├─ config.py      # 配置加载模块
│  ├─ run.py         # 启动脚本
│  └─ requirements.txt
├─ secrets/          # 敏感凭据（config.example.yaml 提交，实际文件 gitignore）
├─ frontend/         # Vue 3 前端
│  ├─ src/           # 源码（views / components / store / api / router）
│  ├─ tests/         # Vitest 单元测试
│  ├─ public/
│  └─ package.json
├─ mobile/           # Flutter 移动端
│  └─ lib/           # phone / windows / component / core / data / providers / services
├─ deploy/           # 部署工件（Dockerfile / compose / nginx / systemd）
├─ docs/             # 项目文档
└─ .github/workflows # CI
```

## 关键数据流

### 文件流媒体

`GET /api/file/data?file_id=X` → 查 diskcache 缓存 → 查 DB 获取文件路径 → 请求 WebDAV 302 → 缓存 URL → 返回重定向。失败时回退到随机图片/视频降级地址。

### 媒体列表

`GET /api/media/list` → `get_media_list()` 批量查询 items，再并行批量查询 links / files / userdata / aliases，经 `app/schemas/media.py` 序列化。

- 支持 keyset 分页（`cursor` + `next_cursor`，`date_created`/`order` 排序），不传时回退 offset
- `fetch_files_batch` 显式列选择，避免回拉 `FFmpeg` 大 JSON

### 媒体统计

`GET /api/media/stats` → 生产模式缓存 60s（diskcache），debug 模式直接查询保证一致性。

### 认证

JWT access + refresh 双 token。移动端通过 Dio 拦截器自动刷新；前端通过 Axios 拦截器 + 订阅队列刷新。

## 配置机制

三级加载：`CONFIG_PATH` 环境变量 > `config/local.yaml` > `config/default.yaml`，随后合并 `secrets/config.yaml` 覆盖。详见 [backend/config/README.md](../backend/config/README.md)。
