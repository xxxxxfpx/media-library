# 开发指南

## 环境要求

- Python 3.10+（Windows 下建议使用 `backend/.venv`，勿用裸 `python`）
- Node.js 20+
- Flutter 3.x（Dart 3.11+）

## 0. 准备密钥（必做）

应用启动守卫要求 `secret_key` 非空，否则拒绝启动：

```bash
cp secrets/config.example.yaml secrets/config.yaml   # 填入随机 secret_key 与 admin 密码
```

> `secrets/config.yaml` 已被 gitignore，不会入库。生成随机密钥：
> `python -c "import secrets; print(secrets.token_urlsafe(48))"`

## 后端

```bash
cd backend

# 创建虚拟环境并安装依赖
python -m venv .venv
.\.venv\Scripts\activate        # Windows
source .venv/bin/activate       # Linux/macOS
pip install -r requirements.txt

# 本地配置（可选，复制示例）
copy config\local.example.yaml config\local.yaml

# 启动（热重载）
python run.py
# 或
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

默认账户：`admin` / `admin123`（首次启动自动创建，密码为空时使用默认值）。

> Windows 注意：必须用 `backend\.venv\Scripts\python.exe` 执行，裸 `python` 可能不在 venv 中。ruff 不在 venv（CI 单独安装），本地 `ruff check` 需先 `pip install ruff`。

## 前端

```bash
cd frontend
npm install
npm run dev       # http://localhost:5173，代理 /api -> :8000
npm run lint      # ESLint（lint:fix 自动修复）
npm run test      # Vitest
npm run build     # 生产构建
```

> 5173 若被其他项目占用，换端口：`npm run dev -- --port 5174 --strictPort`。

## 移动端

```bash
cd mobile
flutter pub get
flutter run
flutter analyze
flutter test
```

## 测试

```bash
cd backend
.\.venv\Scripts\python.exe -m pytest            # 后端测试（CONFIG_PATH 指向 env.yaml）
.\.venv\Scripts\python.exe -m pytest tests/test_x.py::TestX::test_y -v   # 单个测试
```

> **既有测试债**：基线约 37 failed / 48 passed，属既存问题，改动后失败数超过 37 才需排查回归。

## 数据库迁移

```bash
cd backend
.\.venv\Scripts\python.exe -m alembic -c database/alembic.ini upgrade head
```

## 数据脚本

`backend/scripts/` 下按职责分为：

| 目录 | 用途 |
|------|------|
| `checks/` | 数据校验/修复脚本 |
| `migrations/` | 一次性数据迁移脚本 |
| `tools/` | 开发辅助工具 |
| `legacy/` | 引用已删除 ORM 字段的旧脚本（存档，**勿运行**） |

> 涉及远程数据源的脚本（含硬编码远程连接）不要随意运行，需先确认源可用。
