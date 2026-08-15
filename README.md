# 媒体库管理系统 (media-library)

基于 FastAPI + Vue 3 + Flutter 的媒体库管理系统，支持电影/剧集/音乐/图片/电子书等多类型媒体的管理、WebDAV 流媒体播放、用户播放记录与云端设置同步。

## 目录结构

```text
media-library/
├─ backend/    # FastAPI 后端（app / database / tests / scripts / config）
├─ frontend/   # Vue 3 前端（views / components / store / api）
├─ mobile/     # Flutter 移动端（phone / windows / component / core / data）
├─ deploy/     # 部署工件（Docker / compose / nginx / systemd）
├─ docs/       # 项目文档
└─ .github/    # CI 工作流
```

## 快速开始

### 后端

```bash
cd backend
python -m venv .venv
.\.venv\Scripts\activate          # Windows
pip install -r requirements.txt
python run.py                     # http://localhost:8000
```

### 前端

```bash
cd frontend
npm install
npm run dev                       # http://localhost:5173（代理 /api -> :8000）
```

### 移动端

```bash
cd mobile
flutter pub get
flutter run
```

默认账户：`admin` / `admin123`

## 文档

- [docs/README.md](docs/README.md) — 文档索引
- [docs/architecture.md](docs/architecture.md) — 架构
- [docs/development.md](docs/development.md) — 开发指南
- [docs/deployment.md](docs/deployment.md) — 部署
- [docs/operations.md](docs/operations.md) — 运维

## License

见 [LICENSE](LICENSE)。
