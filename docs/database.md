# 数据库设计

## 表结构（SQLAlchemy 模型）

- `MediaItems` — 所有媒体实体单表（Movie/Series/Season/Episode/Audio/Photo/Book/Person/Genre/Studio/Tag/BoxSet/Source），以 `Type` 枚举区分
- `ItemLinks` — 媒体多对多关联（人物/类型/季/来源等），含 `PeopleType`/`PeopleRole`/`SourceLink`
- `Files` — 文件记录，含 `FFmpeg` 元数据
- `FileLinks` — 文件与媒体关联（含 `ImageType`/`ImageIndex` 等）
- `UserData` — 用户播放数据（复合主键 UserId+ItemId：收藏、进度、评分、播放次数）
- `Users` — 用户（PBKDF2-SHA256 加盐哈希）

> 软删除：`MediaItem.IsDeleted` 标记，所有查询默认过滤。

## Alembic 迁移

```bash
cd backend/database
alembic revision --autogenerate -m "description"
alembic upgrade head
```

> `alembic.ini` 中 `sqlalchemy.url` 为空，实际连接来自 `config` 模块（`env.py` 从 `config.py` 读取）。历史迁移链与当前 ORM 模型存在偏差，构建新库时优先使用 `init_db()`（应用 lifespan 自动执行）。

## 数据脚本

见 [development.md](development.md) 中的 `scripts/` 目录说明。`scripts/legacy/` 为旧模型脚本存档，勿运行。
