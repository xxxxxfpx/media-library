# 部署指南

## Docker Compose

```bash
# 1. 构建前端产物
cd frontend && npm ci && npm run build && cd ..

# 2. 准备配置与密钥
cp backend/secrets/config.example.yaml backend/secrets/config.yaml   # 填入真实凭据
cp backend/config/local.example.yaml backend/config/local.yaml       # 生产覆盖
cp deploy/.env.example deploy/.env                                   # 生产环境变量

# 3. 启动
cd deploy
docker compose up -d --build
```

- 后端：`http://localhost:8000`
- 前端（nginx 静态 + 反代）：`http://localhost:3000`

## systemd（单机裸部署）

```bash
sudo cp deploy/systemd/media-manager-backend.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now media-manager-backend
```

按实际路径修改服务文件中 `WorkingDirectory` / `ExecStart` / 用户。

## 反向代理（nginx）

示例见 `deploy/nginx.conf`（SPA 回退 + `/api` 反代 + 流媒体禁缓冲）。

## 生产配置要点

- 设置 `CONFIG_PATH` 指向 `config/local.yaml`
- 将 `app.debug` 设为 `false`
- 通过 `secrets/config.yaml` 注入云盘与远程库凭据
- 数据库改用 PostgreSQL 时更新 `database.*` 配置
- 前置一层 HTTPS 反向代理
