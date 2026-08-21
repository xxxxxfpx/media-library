# Repository Instructions

## Scope

- `backend/` 是 FastAPI + SQLAlchemy async 后端；`frontend/` 是 Vue 3 + Vite；`mobile/` 是 Flutter 客户端。
- 后端路由在 `backend/app/api/`，业务逻辑在 `backend/app/services/`，数据库模型在 `backend/database/models/`，迁移在 `backend/database/alembic/`。
- `CLAUDE.md` 包含更完整的架构与数据流说明；修改架构时同步检查它和本文件。

## Run And Verify

- Windows 后端必须使用虚拟环境解释器，不要依赖裸 `python`：`cd backend; .\.venv\Scripts\python.exe run.py`。
- 后端默认监听 `http://localhost:8000`；`run.py` 会启动 Uvicorn reload，但**后端已经启动后，任何代码修改仍必须手动重启后端再验证**。
- 前端：`cd frontend; npm install; npm run dev`，默认监听 `http://localhost:5173`，`/api` 代理到 `localhost:8000`。
- 前端依赖缺失或出现 Rollup Windows 原生可选依赖错误时，先在 `frontend/` 执行 `npm install`，不要删除 lockfile。
- 后端全量测试：`cd backend; .\.venv\Scripts\python.exe -m pytest`。
- 后端单测：`cd backend; .\.venv\Scripts\python.exe -m pytest tests/test_x.py::TestX::test_y -v`。
- 前端检查：`cd frontend; npm run lint`、`npm run test`、`npm run build`。
- 移动端检查：`cd mobile; flutter analyze; flutter test`；需要运行时先 `flutter pub get`。
- 改动数据库 schema 后，先在 `backend/` 执行 `cd backend; .\.venv\Scripts\alembic.exe -c database\alembic.ini upgrade head`，再重启后端并运行相关测试。

## Configuration And Secrets

- 配置优先级：`CONFIG_PATH` -> development 模式的 `backend/env.yaml` -> `backend/config/local.yaml` -> `backend/config/default.yaml`。
- `secrets/config.yaml` 是 gitignored 敏感覆盖，模板是 `secrets/config.example.yaml`；不要把 secret、管理员密码、云盘凭据或远程数据库凭据写入代码、日志或提交。
- 后端启动要求非空 `app.secret_key`；缺少密钥会在 lifespan 中直接拒绝启动。
- 测试通过 `backend/tests/conftest.py` 设置 `CONFIG_PATH=backend/env.yaml`，不要用生产配置替代测试配置。
- 生产 CORS 通过逗号分隔的 `CORS_ORIGINS` 设置；本地默认只允许前后端 localhost 来源。
- 默认账户通常是 `admin` / `admin123`，应用启动时会在不存在时创建；以本地 secrets 配置为最终准值。

## Database And API Gotchas

- 默认数据库是 `backend/data/database/media.db`；SQLite 连接启用 WAL、`busy_timeout=5000` 和外键约束，生产可切 PostgreSQL。
- 使用 Alembic 管理 schema，不要只修改 ORM 模型或直接手改数据库；迁移配置位于 `backend/database/alembic.ini`。
- `/api/file/data`、`/api/media/stats`、`/api/system/info` 需要登录；媒体二进制 URL 还支持 `token` query 参数，因为 `<img>`、`<video>` 和 Flutter 网络图片不能带 Authorization header。
- `/api/media/list` 支持 `cursor` keyset 分页；不传 cursor 才使用 offset 兼容路径。生产 stats 缓存 60 秒，debug 模式不缓存。
- 文件可能由第三方云盘托管：`Files.Provider` + `ProviderFileId` 是稳定身份，临时播放 URL 不应作为永久标识；`DriveFiles` 保存云盘映射。
- 云盘/远程数据库脚本必须从环境变量读取凭据；运行远程脚本前确认数据源可用，禁止运行 `backend/scripts/legacy/` 下脚本。

## Workflow

- 先读相关路由、service、schema、model 和迁移，再改代码；保持 API 路由薄，复用 service 层和 `get_db_session`。
- 改动后至少运行受影响的单测；涉及后端启动或 schema 的改动同时重启后端并检查 `http://localhost:8000` 的实际响应。
- `ruff` 不随 venv 保证存在；本地需要时先安装，再执行 `ruff check app database tests`。
- `frontend/.env`、`backend/env.yaml` 和 `secrets/config.yaml` 均为本地覆盖，不要提交。
- 提交信息遵循 `{type}({keyword}):{中文摘要}`，随后每行一条中文修改说明；除非用户要求，不要自行提交或修改 git 历史。
- **推送后必须检查 GitHub Actions 状态**：每次 `git push` 完成后，立即查看 GitHub Actions 工作流运行结果，确保 CI 和 Docker Deploy 成功；若失败需排查并修复后重新推送。

## High-Value References

- `README.md`：快速开始与功能边界。
- `CLAUDE.md`：接口、目录和数据流细节。
- `MIGRATION_PLAN.md`：全量迁移计划。
- `docs/`：架构、开发、部署和运维文档。
