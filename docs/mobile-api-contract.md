# 移动端 API 契约同步

## 后端最新
- `GET /api/media/list` 支持 `cursor` keyset 分页，返回 `next_cursor`
- `GET /api/media/info` / `stats` / `/api/user/setting` / `/api/file/data` 保持

## 移动端已同步
- `MediaListResponse` 新增 `nextCursor`，解析 `next_cursor`
- `MediaApi.getList` 新增可选 `cursor` 参数
- `MediaApi` 超时待接入 `Config.load()` 的 15/30s 配置（已规划）

## 待完成
- 网格/横向区块优先使用 cursor 分页，保留 offset 兼容
- 统一图片 URL 生成（TokenCache + baseUrl）
- 合并 TokenCache/TokenManager/AuthService 为 SessionManager
- 校验 `ffmpeg` 字段类型（String vs Map）统一解析
