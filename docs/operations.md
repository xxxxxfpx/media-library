# 运维手册

## 健康检查

```bash
curl http://localhost:8000/health
# {"status": "ok", "version": "1.0.0"}
```

## 日志

- 应用日志：`backend/data/log/app.log`（Rotating 50MB×3）与控制台；级别随 `app.debug` 联动，可用 `logging.level` 显式覆盖
- 每个请求生成 `request_id`（响应头 `X-Request-ID`），通过 `rg "req_id=<id>" backend/data/log/app.log` 还原单请求全链路（含 DB/出站调用）；与请求无关的上下文记为 `req_id=-`
- SQL 日志：`app.debug=true` 时随 `sqlalchemy.engine` 输出到 `app.log`（含 `req_id`），生产（INFO）不记录 SQL
- 文件数据追踪：`backend/data/log/file_data.log`（含 `file_id` 维度）
- 登录成功/失败、限流、批量创建等安全与写操作均有审计打点

## 运行时数据

`backend/data/`：

| 路径 | 内容 |
|------|------|
| `data/database/media.db` | SQLite 数据库（WAL 模式，含 -wal/-shm 伴随文件） |
| `data/cache/file_url` | WebDAV URL 缓存（diskcache） |
| `data/cache/media_stats` | 媒体统计缓存（diskcache，生产模式） |
| `data/log/` | 日志 |

> 缓存可安全删除；数据库需定期备份。备份 SQLite 时建议先检查点 WAL（`PRAGMA wal_checkpoint`）或停服复制。

## 备份

- SQLite：直接复制 `media.db`（建议先停服或使用 SQLite 在线备份）
- PostgreSQL：`pg_dump`
- 配置与密钥：`backend/config/`、`secrets/`

## 常用运维脚本

```bash
cd backend
.\.venv\Scripts\python.exe scripts\checks\check_db_status.py     # 数据库状态
.\.venv\Scripts\python.exe scripts\checks\check_db_stats.py      # 数据统计
```

> `scripts/legacy/` 与远程源相关脚本请勿在生产直接运行。
