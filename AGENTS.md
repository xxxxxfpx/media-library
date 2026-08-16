# AGENTS.md

## 启动命令

- **后端**: `cd backend && python run.py`（运行在 `http://localhost:8000`，入口 `app.main:app`）
- **后端测试**: `cd backend && .\.venv\Scripts\python.exe -m pytest`
- **单个后端测试**: `cd backend && .\.venv\Scripts\python.exe -m pytest tests/test_x.py::TestX::test_y -v`
- **前端**: `cd frontend && npm install && npm run dev`（运行在 `http://localhost:5173`，代理 `/api` 到后端）
- **前端 lint**: `cd frontend && npm run lint`（自动修复用 `npm run lint:fix`）
- **前端测试**: `cd frontend && npm run test`（Vitest）
- **前端构建**: `cd frontend && npm run build`
- **移动端**: `cd mobile && flutter analyze && flutter test`

Windows 注意：必须显式用 `backend\.venv\Scripts\python.exe`，裸 `python` 可能不在 venv 中。

## 提交规范

提交信息遵循 `{提交类型}({提交关键词}):{提交摘要[中文]}`，随后每行一条中文修改条目点。示例：

```
fix(auth): 修复刷新令牌校验
- 刷新 token 时校验用户 IsActive
- 未激活用户禁止续期
```

## 默认账户

`admin` / `admin123`（应用启动时若不存在则自动创建）。

## 配置与密钥

- 配置加载优先级：`CONFIG_PATH` 环境变量 → `ENV=development` 时的 `backend/env.yaml` → `backend/config/local.yaml` → `backend/config/default.yaml`。
- 敏感配置在 `secrets/config.yaml`（gitignored，含真实 `secret_key`、admin 密码、`cloud_auth`、`remote_database`），会合并到所选配置之上；模板为 `secrets/config.example.yaml`，可用 `SECRETS_PATH` 覆盖路径。
- **启动守卫**：`app.main` lifespan 在 `app.secret_key` 为空时直接 `raise RuntimeError`——未配置密钥则拒绝启动。
- 测试能启动是因为 `tests/conftest.py` 设 `CONFIG_PATH=backend/env.yaml`，且 secrets 合并提供了非空 `secret_key`。
- 生产 CORS 用 `CORS_ORIGINS` 环境变量（逗号分隔）指定，默认仅 localhost:5173/8000。

## 鉴权注意

- `/api/file/data`、`/api/media/stats`、`/api/system/info` 均需登录。
- `/api/file/data` 额外接受 `token` query 参数：浏览器 `<img>`/`<video>` 与 Flutter `Image.network` 无法带 Authorization 头，前端/移动端构建媒体 URL 时以 `&token=<access_token>` 附加。移动端通过 `mobile/lib/core/token_cache.dart` 全局缓存取 token。

## 架构

- `backend/app/` — FastAPI 应用，路由在 `app/api/`，服务逻辑在 `app/services/`；路由薄、逻辑在 service，依赖用 `app/api/deps.py` 的 `get_db_session`
- `backend/database/` — SQLAlchemy async 模型与引擎；Alembic 迁移在 `database/alembic/`（`alembic.ini` 同目录）
- `backend/config/` — 配置（`default.yaml` 默认、`local.yaml` 本地覆盖、`setting.yaml` UI 卡牌配置）
- `secrets/` — 敏感凭据（仅 `config.example.yaml` 提交）
- `backend/scripts/` — 数据校验/迁移脚本（checks / migrations / tools / legacy）
- `frontend/` — Vue 3 + Vite 前端，API 代理到 `localhost:8000`
- `mobile/` — Flutter 移动端
- 详细的接口/数据流说明见 `CLAUDE.md`（架构部分更全，两者需同步维护）

## 数据库

- 默认 SQLite（`backend/data/database/media.db`），通过 `database/core.py` 的 async engine 访问
- **SQLite 已启用 WAL + `busy_timeout=5000` + `foreign_keys=ON`**（`core.py` 连接事件监听设置）；连接池按库型分流（SQLite 5+5，PG 32）
- 生产可切换 PostgreSQL（`config/local.yaml` 中 `database.type: postgresql`）
- `requirements.txt` 含 `psycopg2-binary`（供 Alembic 同步引擎迁移 PG 用）与 `alembic`
- **视频化精简**：`MediaType`/`FileType` 枚举已删音乐/照片/书籍/频道等类型，`MediaItems.AlbumId` 列已移除（迁移 `video_only_schema`）
- **列表分页**：`/api/media/list` 支持 `cursor` 参数（keyset 分页，`next_cursor` 返回）；不传时走 `offset` 兼容。keyset 仅对 `date_created`/`order` 排序生效
- **stats 缓存**：`get_media_stats` 在 debug=false（生产）时缓存 60s，debug 模式不缓存保证测试一致性

## 测试状态（重要）

- **基线为 85 passed / 0 failed**（2026-08-16 修复全部 37 个失败测试后）。此前基线为 37 failed / 48 passed（既存测试债）。
- CI 后端 job（`pytest -q`）应保持绿灯；改动后若出现失败需排查回归。

## 数据验证/修复脚本

`backend/scripts/` 下按职责分类：`checks/`（校验）、`migrations/`（迁移）、`tools/`（工具）、`legacy/`（存档，勿运行）。涉及远程数据库的脚本凭据通过环境变量 `REMOTE_DB_HOST/PORT/NAME/USER/PASSWORD` 读取（未设置则失败），不得硬编码凭据。涉及远程数据源的脚本先确认源可用。

## 其他注意事项

- **ruff 不在 venv**：本地 `ruff check` 需先 `pip install ruff`；CI 单独安装 ruff（`ruff check app database tests`）。
- pytest 配置在 `backend/pytest.ini`（`asyncio_mode = auto`）。
- `frontend/.env` 与 `backend/env.yaml` 均为本地覆盖，不入库。

## 重要文件

- `MIGRATION_PLAN.md` — 全量迁移计划文档
- `CLAUDE.md` — 架构/数据流详解（与 AGENTS.md 保持同步）
- `docs/` — 项目文档（架构/开发/部署/运维）
