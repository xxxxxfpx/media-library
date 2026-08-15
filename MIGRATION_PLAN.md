# 数据库迁移计划

## 一、远程数据库概况

**数据库信息:**
- 主机: 47.120.67.251:5432
- 数据库: emby
- 表数量: 14个
- 核心数据量:
  - MediaItems: 24,832 条媒体记录
  - Files: 50,450 条文件记录
  - ItemLinks: 281,186 条关联记录
  - ItemPeople: 16,273 条人物关联
  - FileImages: 33,511 条文件图片

---

## 二、核心表结构对比

### 1. Users (用户表)

| 远程表字段 | 本地表字段 | 映射关系 | 处理方式 |
|-----------|-----------|---------|---------|
| Id | Id | 1:1 | 直接复制 |
| Username | Name | 重命名 | Username → Name |
| Password | PasswordHash | 需处理 | 需确认密码格式兼容性 |
| Email | Email | 1:1 | 直接复制 |
| IsAdmin | IsAdmin | 1:1 | 直接复制 |
| IsDisabled | - | 无对应 | 映射为 IsActive = !IsDisabled |
| LastLoginDate | - | 无对应 | 忽略 |
| ProfileImage | - | 无对应 | 忽略 |

**差异说明:**
- 远程使用简单Password字段，本地使用PasswordHash+Salt
- 本地多了Setting(JSON)字段，可留空

### 2. MediaItems (媒体主表)

| 远程字段 | 本地字段 | 映射 | 说明 |
|---------|---------|-----|------|
| Id | Id | 1:1 | 主键 |
| Guid | - | 忽略 | 本地不使用 |
| Type | Type | 需转换 | USER-DEFINED枚举需映射 |
| Name | Name | 1:1 | 直接复制 |
| OriginalTitle | OriginalTitle | 1:1 | 直接复制 |
| SortName | SortName | 1:1 | 直接复制 |
| Overview | Overview | 1:1 | 直接复制 |
| Tagline | Tagline | 1:1 | 直接复制 |
| ProductionYear | ProductionYear | 1:1 | 直接复制 |
| PremiereDate | PremiereDate | 1:1 | 直接复制 |
| EndDate | EndDate | 1:1 | 直接复制 |
| RunTimeTicks | RunTimeTicks | 1:1 | 直接复制 |
| OfficialRating | OfficialRating | 1:1 | 直接复制 |
| CommunityRating | CommunityRating | 1:1 | 直接复制 |
| CriticRating | CriticRating | 1:1 | 直接复制 |
| DateCreated | DateCreated | 1:1 | 直接复制 |
| DateModified | DateModified | 1:1 | 直接复制 |
| Path | - | 忽略 | 本地不存储 |
| ParentId | - | 忽略 | 层级关系用ItemLinks处理 |
| SeriesId | - | 忽略 | 通过ItemLinks关联 |

**关键差异:**
- 远程使用`Guid`字段作为全局唯一标识，本地不使用
- 远程有大量Emby特有字段（IsMovie, IsSeries等），本地简化
- 远程Type为USER-DEFINED，本地为枚举类型

### 3. Files (文件表)

| 远程字段 | 本地字段 | 映射 | 说明 |
|---------|---------|-----|------|
| Id | Id | 1:1 | 主键 |
| Etag | Etag | 1:1 | 直接复制 |
| Size | Size | 1:1 | 直接复制 |
| Name | Name | 1:1 | 直接复制 |
| SortName | SortName | 1:1 | 直接复制 |
| Path | Path | 1:1 | 直接复制 |
| CloudId | CloudId | 1:1 | 直接复制 |
| Type | Type | 需转换 | USER-DEFINED → Enum |
| Data | FFmpeg | 需提取 | Data字段为JSON，需提取FFmpeg信息 |

**差异说明:**
- 远程`Data`字段存储JSON格式FFmpeg信息，本地使用FFmpeg字段
- 远程有额外的Width/Height字段（已移除）

### 4. ItemLinks (关联表)

| 远程字段 | 本地字段 | 映射 | 说明 |
|---------|---------|-----|------|
| ItemId | ItemId | 1:1 | 主键1 |
| LinkedItemId | LinkedItemId | 1:1 | 主键2 |
| Order | - | 忽略 | 本地无排序字段 |

**远程特有功能:**
- 远程使用此表关联所有类型（Source, Season, Episode等）
- 本地有扩展字段：Type, PeopleType, PeopleRole

### 5. ItemPeople (人物关联表) → 合并到 ItemLinks

| 远程字段 | 本地字段 | 映射 | 说明 |
|---------|---------|-----|------|
| ItemId | ItemId | 1:1 | - |
| PersonId | LinkedItemId | 重命名 | PersonId → LinkedItemId |
| Role | PeopleRole | 1:1 | 直接复制 |
| Type | PeopleType | 1:1 | 转换为Actor/Director等 |
| Order | - | 忽略 | - |

**迁移策略:**
- 将ItemPeople数据转换为ItemLinks格式
- Type字段映射为'Person'
- PeopleType保持原值

### 6. FileImages (文件图片表) → 合并到 FileLinks

| 远程字段 | 本地字段 | 映射 | 说明 |
|---------|---------|-----|------|
| ItemId | ItemId | 1:1 | - |
| FileId | FileId | 1:1 | - |
| Type | ImageType | 1:1 | USER-DEFINED → Enum |
| ImageIndex | ImageIndex | 1:1 | 直接复制 |

**迁移策略:**
- 将FileImages数据转换为FileLinks格式
- 添加默认Id字段

### 7. UserData (用户数据表)

| 远程字段 | 本地字段 | 映射 | 说明 |
|---------|---------|-----|------|
| UserId | UserId | 1:1 | 复合主键1 |
| ItemId | ItemId | 1:1 | 复合主键2 |
| IsFavorite | IsFavorite | 1:1 | 直接复制 |
| PlaybackPositionTicks | PlaybackPositionTicks | 1:1 | 直接复制 |
| PlayCount | PlayCount | 1:1 | 直接复制 |
| Played | IsPlayed | 重命名 | Played → IsPlayed |
| Rating | Rating | 1:1 | 直接复制 |

**差异说明:**
- 远程有Likes字段，本地使用Rating
- 远程有LastPlayedDate等时间字段，本地简化

---

## 三、仅远程存在的表（需特殊处理）

### 1. ItemSources - 来源关联
映射为ItemLinks，Type='Source'

### 2. ItemProviders - 元数据提供者
可选择性迁移或忽略（本地无对应表）

### 3. Providers - 提供者列表
可选择性迁移或忽略

### 4. FileStreams - 文件流信息
可忽略（本地使用FFmpeg字段存储）

### 5. Chapters - 章节信息
可忽略（本地不支持）

### 6. ListItems - 列表项
可忽略（本地不支持播放列表）

---

## 四、仅本地存在的表

### 1. Aliases (别名表)
远程无对应表，需从远程Name字段提取或留空

### 2. FileLinks (文件关联)
从FileImages迁移

### 3. UserItemShares (分享表)
远程无对应功能，留空

---

## 五、迁移步骤计划

### 阶段1: 准备工作
1. 备份当前本地数据库
2. 创建迁移脚本
3. 测试连接远程数据库

### 阶段2: 数据迁移

**Step 1: Users (用户)**
```python
# 迁移策略
- 仅迁移必要的用户（排除系统用户）
- 密码需要重新处理（Emby密码格式与本地不同）
- 生成新的Salt和PasswordHash
```

**Step 2: MediaItems (媒体)**
```python
# 迁移策略
- 按Id顺序批量迁移
- Type字段映射转换
- 跳过IsDeleted=True的记录
- 处理日期格式转换（timestamp with time zone）
```

**Step 3: Files (文件)**
```python
# 迁移策略
- 批量迁移所有文件记录
- 从Data字段提取FFmpeg信息
- Type字段映射转换
```

**Step 4: ItemLinks (关联)**
```python
# 迁移策略
- 先迁移ItemLinks
- 再迁移ItemPeople（转换为ItemLinks）
- 再迁移ItemSources（转换为ItemLinks）
```

**Step 5: FileLinks (文件关联)**
```python
# 迁移策略
- 从FileImages转换
- 添加自增Id
```

**Step 6: UserData (用户数据)**
```python
# 迁移策略
- 直接迁移
- 字段名转换
```

### 阶段3: 数据校验
1. 记录数对比检查
2. 关键字段完整性检查
3. 关联关系有效性检查

### 阶段4: 清理与优化
1. 重建索引
2. 更新统计信息
3. 优化查询性能

---

## 六、字段类型映射

### MediaType 枚举映射
| 远程值 | 本地值 |
|-------|-------|
| Movie | Movie |
| Series | Series |
| Season | Season |
| Episode | Episode |
| Audio | Audio |
| Video | Video |
| Photo | Photo |
| Book | Book |
| Person | Person |
| Genre | Genre |
| Studio | Studio |
| Tag | Tag |
| Source | Source |

### FileType 枚举映射
| 远程值 | 本地值 |
|-------|-------|
| Video | Video |
| Audio | Audio |
| Image | Image |
| Subtitle | Subtitle |

---

## 七、风险与注意事项

### 1. 密码问题
远程数据库使用Emby的密码格式，需要用户重新登录或重置密码

### 2. 媒体路径
远程Path字段可能指向不同的文件系统，需要验证文件可访问性

### 3. 图片资源
远程FileImages关联的图片文件需要确认能否访问

### 4. 数据库ID冲突
远程和本地的Id都是自增的，需要确保不冲突（使用相同Id）

### 5. 事务处理
建议分批迁移，每批1000条记录，避免事务过大

---

## 八、预计时间与资源

| 步骤 | 预计时间 | 说明 |
|-----|---------|------|
| Users | <1分钟 | 用户数量少 |
| MediaItems | 5-10分钟 | 24K记录 |
| Files | 10-15分钟 | 50K记录 |
| ItemLinks | 15-20分钟 | 280K记录 |
| ItemPeople | 5分钟 | 16K记录 |
| FileImages | 5分钟 | 33K记录 |
| UserData | <1分钟 | 25条记录 |
| **总计** | **40-60分钟** | 含校验时间 |

---

## 九、迁移脚本设计

建议创建 `migrate_data.py` 脚本，功能包括：
1. 连接远程PostgreSQL
2. 连接本地SQLite/PostgreSQL
3. 按步骤执行迁移
4. 实时进度显示
5. 错误处理与回滚机制
6. 迁移报告生成

---

**审核要点:**
1. 是否需要迁移所有历史数据？
2. 密码处理方案确认
3. 媒体文件路径是否需要重新配置？
4. 图片资源存储方式确认
5. 迁移时间窗口安排
