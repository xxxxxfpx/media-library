# 开发指南

## 环境要求

- Python 3.10+
- Node.js 20+
- Flutter 3.x（Dart 3.11+）

## 后端

```bash
cd backend

# 创建虚拟环境并安装依赖
python -m venv .venv
.\.venv\Scripts\activate        # Windows
source .venv/bin/activate       # Linux/macOS
pip install -r requirements.txt
pip install pytest pytest-asyncio ruff

# 本地配置（可选，复制示例）
copy config\local.example.yaml config\local.yaml

# 启动（热重载）
python run.py
# 或
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

默认账户：`admin` / `admin123`（首次启动自动创建，密码为空时使用默认值）。

## 前端

```bash
cd frontend
npm install
npm run dev       # http://localhost:5173，代理 /api -> :8000
npm run lint      # ESLint
npm run test      # Vitest
npm run build     # 生产构建
```

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
pytest            # 后端测试（CONFIG_PATH 指向 env.yaml）
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
