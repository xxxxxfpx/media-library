# 数据库设计

## 表结构（SQLAlchemy 模型）

- `MediaItems` — 视频媒体单表（Movie/Series/Season/Episode/BoxSet/Genre/Person/Studio/Tag/Source 等），以 `Type` 枚举区分
- `ItemLinks` — 媒体多对多关联（人物/类型/季/来源等），含 `PeopleType`/`PeopleRole`/`SourceLink`/`Order`
- `Files` — 文件记录，含 `FFmpeg` 元数据（JSON）
- `FileLinks` — 文件与媒体关联（含 `ImageType`/`ImageIndex`/章节字段）
- `UserData` — 用户播放数据（复合主键 UserId+ItemId：收藏、进度、评分、播放次数）
- `Users` — 用户（PBKDF2-SHA256 加盐哈希）

> **视频化精简**：`MediaType`/`FileType` 枚举仅保留视频相关类型（音乐/照片/书籍/频道等已移除），`MediaItems.AlbumId` 列已删除（迁移 `video_only_schema`）。
>
> 软删除：`MediaItem.IsDeleted` 标记，所有查询默认过滤。

## 索引

除模型内置索引外，迁移 `db_optimization_indexes` 追加了面向视频列表查询的组合索引：

| 索引 | 覆盖场景 |
|------|---------|
| `MediaItems(Type, IsDeleted)` | 列表热路径类型过滤 + 软删除 |
| `MediaItems(Type, IsDeleted, DateCreated)` | 上述 + 默认 `date_created` 排序 |
| `ItemLinks(LinkedItemId, ItemId)` | 反向子项/`has_children` 查询 |
| `ItemLinks(LinkedItemId, Order)` | 季/集按 `Order` 排序 |
| `UserData(ItemId, UserId)` | 批量回填用户数据 |
| `FileLinks(ItemId, FileId)` | 批创建去重/存在性检查 |

## 运行优化

- **WAL 模式**：`database/core.py` 连接事件设置 `journal_mode=WAL` + `busy_timeout=5000` + `foreign_keys=ON`
- **连接池分流**：SQLite 用小连接池（5+5），PostgreSQL 用 32
- **keyset 分页**：`/api/media/list` 支持 `cursor` 参数（`date_created`/`order` 排序），避免深分页 O(n) 扫描
- **统计缓存**：`get_media_stats` 生产模式缓存 60s（debug 模式不缓存，保证测试一致性）

## Alembic 迁移

```bash
cd backend
.\.venv\Scripts\python.exe -m alembic -c database/alembic.ini upgrade head
```

> `alembic.ini` 中 `sqlalchemy.url` 为空，实际连接来自 `config` 模块（`env.py` 从 `config.py` 读取）。历史迁移链与当前 ORM 模型存在偏差，构建新库时优先使用 `init_db()`（应用 lifespan 自动执行）。

## 数据脚本

见 [development.md](development.md) 中的 `scripts/` 目录说明。`scripts/legacy/` 为旧模型脚本存档，勿运行。

- `scripts/checks/check_video_only_prep.py` — 视频化迁移前置检查（类型分布 / AlbumId 检测）
