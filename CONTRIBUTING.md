# 贡献指南

感谢您参与 **media-library**（媒体库管理系统）的开发。请遵循以下约定，保持代码库整洁、可维护。

## 目录结构

仓库为单仓（monorepo）结构：

| 目录 | 说明 |
|------|------|
| `backend/` | FastAPI 后端（app / database / tests / scripts / config） |
| `frontend/` | Vue 3 前端（src / tests） |
| `mobile/` | Flutter 移动端（lib / test / android / ios 等） |
| `deploy/` | 部署工件（Docker / compose / nginx / systemd） |
| `docs/` | 项目文档（架构 / 开发 / 部署 / 运维 / 参考） |
| `secrets/` | 敏感凭据（仅提交示例，真实文件被 gitignore） |

## 本地开发

### 后端

```bash
cd backend
python -m venv .venv
pip install -r requirements.txt
python run.py            # http://localhost:8000
```

运行测试（注意：存在既存测试债，基线为 37 failed / 48 passed，非本次改动引入）：

```bash
cd backend
.venv/Scripts/python.exe -m pytest          # Windows
.venv/bin/python -m pytest                  # Linux/macOS
```

### 前端

```bash
cd frontend
npm install
npm run dev             # http://localhost:5173（代理 /api -> :8000）
npm run lint            # ESLint（自动修复：npm run lint:fix）
npm run test            # Vitest
npm run build           # 生产构建
```

### 移动端

```bash
cd mobile
flutter pub get
flutter analyze
flutter test
```

## 代码规范

- **后端**：遵循 `backend/pyproject.toml` 中的 ruff 配置（`ruff check app database tests`）。新增依赖同步更新 `requirements.txt` 与 `pyproject.toml`。
- **前端**：ESLint（`vue3-essential` + `eslint-config-prettier`）+ Prettier。提交前执行 `npm run lint`。
- **移动端**：提交前执行 `flutter analyze` 与 `flutter test`。
- 新功能应附带测试；后端测试遵循 `pytest.ini`（`asyncio_mode = auto`）。

## 提交规范

提交信息遵循 `{提交类型}({提交关键词}):{提交摘要[中文]}`，随后每行一条中文修改条目。示例：

```
fix(auth): 修复刷新令牌校验
- 刷新 token 时校验用户 IsActive
- 未激活用户禁止续期
```

常用类型：`feat`（新功能）、`fix`（缺陷修复）、`refactor`（重构）、`docs`（文档）、`test`（测试）、`ci`（CI 配置）。

## 分支与 PR

- 直接提交 `main` 前请确保本地 CI 相关检查（后端 pytest、前端 lint/test/build）通过。
- 较大的功能改动建议开分支，并通过 PR 合并。

## 配置与密钥安全

- 真实凭据（`secret_key`、admin 密码、云盘账号、远程数据库）只写入 `secrets/config.yaml`，该文件已被 `.gitignore` 忽略。
- 不要提交任何 `.env`、`config/local.yaml`、`secrets/config.yaml` 等本地覆盖文件。
- 涉及远程数据源的脚本（`backend/scripts/`）不得硬编码凭据，统一通过 `REMOTE_DB_*` 环境变量读取。

## 其他

- 完整架构说明见 `docs/` 与 `CLAUDE.md`；启动命令与提交规范的最新版本见 `AGENTS.md`。
