# Media Library Agent API Guide（实战手册）

本手册面向 AI Agent。目标：给定一个网页 URL，提取其中的视频 / 图片 / 简介等信息，
规范化后写入媒体库。按本手册的顺序执行即可完整走通流程。

---

## 0. 快速开始

**Base URL（重要）**

- 生产环境：`https://media.mz727.top`
- 本地开发：`http://localhost:8000`

下文所有接口路径均相对 Base URL。本文以生产地址为例。

**参考**

- 完整接口清单（含全部参数与枚举）：`GET {base}/openapi.json`
- 健康检查（无需认证）：`GET {base}/health`

---

## 1. 认证与 Token

所有 `/api/*` 业务接口（除 `/llm.txt`、`/health`、媒体二进制带 token 访问外）都需要认证。

### 1.1 登录

```
POST {base}/api/user/login
Content-Type: application/json

{"username": "admin", "password": "<密码>"}
```

成功响应：

```json
{
  "access_token": "eyJ...",
  "refresh_token": "eyJ...",
  "token_type": "bearer"
}
```

后续所有请求携带：

```
Authorization: Bearer <access_token>
```

### 1.2 Token 过期处理（重要）

- `access_token` 有效期较短，过期后接口返回 `401`。
- 收到 `401` 时，用 `refresh_token` 换新：

```
POST {base}/api/user/refresh
Content-Type: application/json

{"refresh_token": "<refresh_token>"}
```

- 返回新的 `access_token` / `refresh_token`，更新本地保存后重试原请求。
- 不要拿同一个 access_token 反复重试 `401` 的请求。

### 1.3 权限

- 媒体创建（`/api/media/batch`）、云盘操作（`/api/drives/guangyapan/*`）需要管理员权限。
- 一般查询（`/api/media/list`、`/api/media/info`）登录即可。

---

## 2. 核心工作流（严格按顺序）

Agent 入库一个网页媒体，必须遵循以下顺序：

```
Step 1  解析网页，提取：标题、简介、视频 URL、图片、tag、人物
  │
Step 2  处理文件（见 §4）
  │      ├─ 公开 URL 视频  → offline 离线下载（异步，轮询）
  │      ├─ 加密/防盗链图片 → upload-bytes 字节上传（同步）
  │      └─ 记录返回的 provider_file_id（稳定身份）与 url（临时可播）
  │
Step 3  创建媒体项（见 §5），引用 Step 2 的文件
  │
Step 4  （可选）创建 Tag / Person 等并通过 item_links 关联
```

**为什么必须先处理文件再建媒体项：** 媒体项里的 `files[].attrs.url` / `provider_file_id`
需要在创建时就有值，文件处理接口会返回这些值。

---

## 3. 媒体类型选用对照表

创建媒体项时，`attrs.type` 决定该条目的语义。Agent 常用：

| type | 用在哪 | 例子 |
|------|--------|------|
| `Movie` | 单部电影 / 单个独立视频 | 一条 YouTube/B站视频 |
| `Series` | 系列 / 多季剧集的父级 | 《荒野求生》整体系列 |
| `Episode` | 系列中的单集 | 某系列的第 3 集 |
| `BoxSet` | 合集 / 打包的多部作品 | 导演合集 |
| `Tag` | 分类标签 | 户外、美食、科技 |
| `Genre` | 题材类型 | 悬疑、纪录片 |
| `Person` | 人物（演员/导演/博主） | 某博主 |
| `Studio` | 出品方 / 频道 | XX工作室 |

**选用规则**

- 一条独立视频 → `Movie`。
- 多个相关视频（同一博主/系列）→ 建一个 `Series`，再为每个视频建 `Episode`，用
  `item_links` 把 Episode 挂到 Series 下（`link` = 父项 temp_id，`linked` = 子项 temp_id）。
- 提取到的分类 → 单独建 `Tag` item，再通过 `item_links` 关联到媒体项。
- 同一批内容里，`Series`/`Episode` 属于"内容结构"，`Tag`/`Genre`/`Person` 属于"元数据关联"。

---

## 4. 文件处理接口（先于媒体创建调用）

### 4.1 上传字节数据（加密图片 / 防盗链内容）— 同步

```
POST {base}/api/drives/guangyapan/upload-bytes
Authorization: Bearer <token>
Content-Type: application/json

{
  "file_data": "<base64 编码的文件内容>",
  "name": "cover.jpg",
  "parent_id": ""
}
```

**适用场景：** 图片 URL 是密文、有防盗链（如抖音 Referer 校验）、或需要浏览器解密后才能拿到内容时，
先用浏览器工具提取 base64 数据，再调用本接口。

**同步语义：** 本接口内部会完成 OSS 上传并轮询等待文件就绪，**返回时即已完成**，
`status` 为 `"ready"`。不需要再轮询。

**限制与必填：**

- `file_data`：base64 编码（`validate=True`，非法 base64 返回 `400`）。
- 上限 **50 MB**（超限返回 `400`）。
- `name`：文件名，**必须含扩展名**（如 `cover.jpg`），用于服务端识别文件类型。
- `parent_id`：可选，留空时使用云盘默认目录。

**成功响应：**

```json
{
  "id": 1,
  "provider": "guangyapan",
  "provider_file_id": "f_abc123",
  "url": "https://.../可播放临时URL...",
  "mode": "upload",
  "name": "cover.jpg",
  "size": 12345,
  "status": "ready"
}
```

**记住 `provider_file_id`（稳定身份）和 `url`（临时可播地址）。**

### 4.2 离线下载 URL（公开 m3u8 / mp4）— 异步，需轮询

```
POST {base}/api/drives/guangyapan/offline/create
Content-Type: application/json

{"url": "https://example.com/video.m3u8", "parent_id": "", "name": "video.mp4"}
```

**适用场景：** 服务器可直接下载的公开视频 URL（m3u8、mp4）。

**异步语义：** 本接口只创建下载任务，**立即返回 `taskId`，不代表下载完成**。
必须轮询进度：

```
POST {base}/api/drives/guangyapan/offline/list
Content-Type: application/json

{"task_ids": ["<taskId>"], "page_size": 10}
```

轮询结果中每条任务的关键字段：

- `status`：`1` = 下载中，`2` = 完成，`-1` / `3` = 失败。
- `fileId`：**出现非空 `fileId` 即代表完成**（status 通常为 `2`）。
- 失败时读取 `errorMessage` / 原因。

**推荐轮询节奏：** 每 5~10 秒一次，任务完成后即可停止。
`/api/drives/guangyapan/offline/delete` 可删除失败/完成的任务。

**注意：** 防盗链站点（如抖音，校验 Referer）服务器直连会失败，请改用 §4.1 的字节上传。

### 4.3 一步式保存（二选一）— 同步

```
POST {base}/api/drives/guangyapan/save-url
Content-Type: application/json

{"url": "https://...", "mode": "offline", "parent_id": "", "name": "video.mp4"}
```

- `mode`：`"offline"` 走离线下载并**同步等待完成**（内部已轮询，成功时返回 `status:"ready"`）；
  `"upload"` 走服务器直传。
- 适合小文件/已验证可下载的 URL；大视频建议用 §4.2 自行控制轮询。
- 成功响应结构与 §4.1 相同。

### 4.4 URL 签名会过期（重要）

- 以上接口返回的 `url` 是**临时可播放地址**，会过期，**不要把它作为永久标识**。
- 稳定身份是 `provider` + `provider_file_id`。
- 需要重新取播放地址时：

```
POST {base}/api/drives/guangyapan/download-url
{"file_id": "<provider_file_id>"}
```

---

## 5. 创建媒体项与关联（核心接口）

```
POST {base}/api/media/batch?strict_graph=true
Authorization: Bearer <token>
Content-Type: application/json
```

一次请求可同时创建多个 item、多个 file、以及它们之间的关联。所有实体先按 `temp_id`
创建，再用 `temp_id` 引用关联。

### 5.1 请求体结构

```json
{
  "source_name": "Agent",
  "items": [
    {
      "temp_id": "item-1",
      "source_info": {
        "source_id": "户外",
        "source_link": "https://example.com/video/123"
      },
      "attrs": {
        "type": "Movie",
        "name": "视频标题",
        "overview": "完整的简介描述，越多越详细越好",
        "tagline": "一句话标语（可选）",
        "premiere_date": "2024-01-01T00:00:00Z",
        "community_rating": 8.5
      }
    }
  ],
  "files": [
    {
      "temp_id": "file-1",
      "attrs": {
        "name": "cover.jpg",
        "type": "Image",
        "provider": "guangyapan",
        "provider_file_id": "f_abc123",
        "url": "https://.../可播URL...",
        "size": 12345
      }
    }
  ],
  "file_links": [
    {
      "item": "item-1",
      "file": "file-1",
      "link_type": "Image",
      "image_type": "Primary"
    }
  ]
}
```

### 5.2 必填字段真相（重要，避免 422/NOT NULL）

**items[].attrs**

- `type`：必填，取值见 §3 对照表（必须与字段名一致，如 `"Movie"`）。
- `name`：强烈建议填（来源 item 可能允许空，但内容媒体项必须有名称）。
- `overview` / `tagline` / `premiere_date` / `community_rating`：均可选。
  `community_rating` 范围 0~10，超出返回 422。
- `attrs` 使用 `extra="forbid"`：**不允许填未定义的字段**，多填会 422。

**files[].attrs**

| 字段 | 必填? | 说明 |
|------|-------|------|
| `name` | ✅ 必填 | 文件名 |
| `type` | ✅ 必填 | 文件类型，如 `Image` / `Video` / `Subtitle` / `Audio` |
| `path` | 视情况 | **数据库层 NOT NULL**。但若提供了 `provider` + `provider_file_id`，服务端自动生成 `drive://{provider}/{provider_file_id}`，无需传；否则**必须传**（如 `/agent/户外/cover.jpg`，注意唯一性，重复 path 会复用旧文件） |
| `provider` | 云盘文件时必填 | `"guangyapan"` |
| `provider_file_id` | 云盘文件时必填 | §4 接口返回的稳定身份 |
| `url` | 可选 | 可播 URL（§4 返回的临时地址） |
| `size` | 可选 | 字节数。**HLS 流无确定大小可省略** |

**file_links[].link_type**

- `"Image"` — 图片，需 `image_type`（`Primary` = 封面）。
- `"MediaSource"` — 媒体源文件（视频本体）。
- `"Chapter"` — 章节，需 `chapter_index`。

### 5.3 去重与更新语义

- 去重键 = `source_name` + `source_id` + `type`。
- 相同键再次提交：**更新已设置的字段**（补全信息），不会重复创建。
- 因此重复爬取同一 URL 是安全的；想补充简介，带相同 `source_id` 重发即可。

### 5.4 source_link 说明（重要）

- `source_link` 作为**请求参数**会被接受，但当前版本**查询接口不回传该字段**
  （数据库未存储此列）。
- 若需在查询侧追溯来源，请依赖 `source_id`（tag 名）与 `source_name`（"Agent"）定位；
  也可以把原始 URL 放进 `overview` 或创建一个 `Alias`。
- 这是已知限制，后续版本会补存储。

### 5.5 成功响应

返回创建结果，包含每个 item 的实际 `id`（`temp_id` 与 `id` 的映射）。后续用 `id` 查询详情。

---

## 6. 查询接口

```
GET {base}/api/media/list?search=<关键词>&limit=50&offset=0
GET {base}/api/media/list?types=Movie&cursor=<next_cursor>   # 游标翻页
GET {base}/api/media/info?id=<id>
GET {base}/api/media/stats
```

- `list` 支持 `cursor` keyset 翻页（响应里的 `next_cursor` 传给下一次请求）。
- `search` 匹配名称 / 简介 / 标语 / 别名。

---

## 7. Agent 数据规范（统一约定）

| 字段 | 值 | 说明 |
|------|-----|------|
| `source_name` | `"Agent"` | 固定值，标识为 Agent 来源，与其他来源隔离 |
| `source_id` | tag 名 | 如 `"户外"`、`"美食"`。多 tag 时建多个 `Tag` item 关联，`source_id` 取主分类 |
| `source_link` | 原始网页 URL | 提交时保留（查询侧当前不回传，见 §5.4） |

---

## 8. 错误处理

### 8.1 错误响应格式

所有错误返回统一结构（FastAPI 默认）：

```json
{"detail": "<错误描述>"}
```

### 8.2 状态码速查

| 状态码 | 含义 | 常见原因与处理 |
|--------|------|----------------|
| `200/201` | 成功 | — |
| `400` | 参数错误 | base64 解码失败、文件超 50MB、云盘未配置 token |
| `401` | 未认证 / token 过期 | 重新登录或用 refresh_token 刷新（§1.2） |
| `404` | 资源不存在 | 查询的 id 不存在 |
| `422` | 请求体校验失败 | 缺必填字段、type 非法、多传未定义字段、评分越界 |
| `502` | 云盘上游错误 | 光鸭 token 失效、目录不存在、离线任务失败；按 detail 排查 |
| `500` | 服务器内部错误 | 重试；持续出现请反馈 |

### 8.3 通用建议

- 收到 `401` → 刷新 token 后重试一次，仍失败则放弃该请求。
- 收到 `422` → 对照 §5.2 必填字段表检查请求体，不要盲目重试。
- 收到 `502` → 光鸭凭据或目录问题，检查 §4.2/§4.3 的任务详情。

---

## 9. 常见坑速查（踩坑汇总）

1. **Base URL**：生产是 `https://media.mz727.top`，不是 `localhost:8000`。
2. **离线下载是异步的**：`offline/create` 返回 taskId ≠ 完成，必须轮询 `offline/list` 直到 `fileId` 非空。
3. **`upload-bytes` 是同步的**：返回即完成（`status:"ready"`），无需轮询。
4. **`path` 字段**：不传 `provider_file_id` 时必须提供；传了则自动生成。
5. **`size` 可省略**：HLS 流没有确定大小，不填即可。
6. **防盗链**：抖音等校验 Referer 的站点离线下载会失败，改用浏览器提取 + `upload-bytes`。
7. **签名 URL 会过期**：保存 `provider_file_id`，播放时用 `download-url` 现取。
8. **先文件后媒体**：`/api/media/batch` 引用文件时，文件必须先处理完成。
9. **`type` 与 `tag`**：`type` 是媒体结构类型（Movie/Series/...）；分类用 `Tag` item 关联。
10. **严格图约束**：`/api/media/batch?strict_graph=true`（默认）要求 items 通过
    item_links 连通；多个独立无关联的 item 会失败，可加关联或设 `strict_graph=false`。

---

## 10. 使用场景对照

| 场景 | 方案 |
|------|------|
| 公开 mp4 / m3u8 视频 | §4.2 离线下载（异步轮询）或 §4.3 save-url(offline) |
| 加密 / 防盗链图片 | §4.1 upload-bytes（浏览器提取 base64） |
| 单条独立视频 | `Movie` + 视频文件 `MediaSource` + 封面 `Image` |
| 系列多集 | `Series` + 多 `Episode`（item_links 挂父子）+ 每集 `MediaSource` |
| 给内容打标签 | `Tag` item + `item_links` 关联 |
| 记录作者/博主 | `Person` item + `item_links` 关联 |

---

*本文档由系统自动生成于 `/llm.txt`，配合 `GET {base}/openapi.json` 使用。*
