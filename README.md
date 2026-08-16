# 媒体库管理系统 (media-library)

基于 **FastAPI + Vue 3 + Flutter** 的视频媒体库管理系统：支持电影/剧集/季/集等视频媒体的管理、123 云盘 WebDAV 流媒体播放、用户播放记录、收藏与云端设置同步。

## 功能特性

- **视频媒体管理**：电影 / 剧集 / 季 / 集 / 合集，单表 + 关联表设计，软删除
- **WebDAV 流媒体播放**：文件通过 302 重定向直连 123 云盘，带 URL 缓存与降级策略
- **双端 UI**：Vue 3 Web 前端 + Flutter 移动端（手机/桌面双布局）
- **完整鉴权**：JWT access + refresh 双令牌，自动刷新；媒体 URL 支持 `token` query 参数（供 `<img>`/`Image.network` 无头场景）
- **用户数据**：播放进度、收藏、评分、历史记录
- **数据库优化**：SQLite WAL、组合索引、keyset 分页、统计缓存；可切换 PostgreSQL

## 技术栈

| 端 | 技术 |
|---|---|
| 后端 | Python FastAPI · SQLAlchemy 2.0 async · JWT (python-jose) · Pydantic v2 |
| 前端 | Vue 3 (Composition API) · Vite · Pinia · Element Plus · Axios |
| 移动端 | Flutter 3.x · Dio · media_kit |
| 数据库 | SQLite (aiosqlite，默认) / PostgreSQL (asyncpg，生产可选) |
| 文件存储 | 123 云盘 WebDAV（302 重定向流式播放） |

## 目录结构

```text
media-library/
├─ backend/    # FastAPI 后端（app / database / tests / scripts / config）
├─ frontend/   # Vue 3 前端（views / components / store / api）
├─ mobile/     # Flutter 移动端（phone / windows / component / core / data）
├─ secrets/    # 敏感凭据（config.example.yaml 提交，实际文件 gitignore）
├─ deploy/     # 部署工件（Docker / compose / nginx / systemd）
├─ docs/       # 项目文档
└─ .github/    # CI 工作流
```

## 快速开始

### 0. 准备密钥

应用启动守卫要求 `secret_key` 非空，否则拒绝启动。首次使用需创建本地密钥文件：

```bash
cp secrets/config.example.yaml secrets/config.yaml   # 填入随机 secret_key 与 admin 密码
```

> `secrets/config.yaml` 已被 gitignore，不会入库。

### 1. 后端

```bash
cd backend
python -m venv .venv
.\.venv\Scripts\activate          # Windows
pip install -r requirements.txt
python run.py                     # http://localhost:8000
```

### 2. 前端

```bash
cd frontend
npm install
npm run dev                       # http://localhost:5173（代理 /api -> :8000）
```

> 若 5173 被其他项目占用，可换端口：`npm run dev -- --port 5174 --strictPort`。

### 3. 移动端

```bash
cd mobile
flutter pub get
flutter run
```

默认账户：`admin` / `admin123`（首次启动自动创建）。

## 配置与密钥

- 配置加载优先级：`CONFIG_PATH` 环境变量 → `ENV=development` 时的 `backend/env.yaml` → `backend/config/local.yaml` → `backend/config/default.yaml`
- 敏感配置在 `secrets/config.yaml`（gitignored），合并到所选配置之上；模板为 `secrets/config.example.yaml`，可用 `SECRETS_PATH` 覆盖路径
- 详见 [docs/development.md](docs/development.md) 与 [backend/config/README.md](backend/config/README.md)

## 文档

- [docs/README.md](docs/README.md) — 文档索引
- [docs/architecture.md](docs/architecture.md) — 架构
- [docs/database.md](docs/database.md) — 数据库设计
- [docs/development.md](docs/development.md) — 开发指南
- [docs/deployment.md](docs/deployment.md) — 部署
- [docs/operations.md](docs/operations.md) — 运维

## 测试状态

后端 pytest 有既存测试债（基线约 37 failed / 48 passed），CI 后端 job 目前为红，属已知问题，非近期改动引入。详见 [AGENTS.md](AGENTS.md)。

## License

[Apache License 2.0](LICENSE)。
