# 单表继承（Single Table Inheritance, STI）设计文档

## 概述

本项目采用 SQLAlchemy 的单表继承（STI）模式设计媒体项数据模型。所有媒体实体（Movie、Series、Season、Episode、Person、Genre、Studio 等）都存储在同一张 `MediaItems` 表中，通过 `Type` 字段区分不同类型。

## 设计决策

### 为什么选择 STI？

1. **查询性能最优**：无需 JOIN 操作，单表查询即可获取所有类型的数据
2. **实现简单**：数据库结构简单，无需维护多张表的关联
3. **类型安全**：Python 层面自动实例化正确类型的对象
4. **代码组织清晰**：每种媒体类型有独立的类，包含特有的属性和方法

### 与 JTI/CTI 的对比

| 特性 | STI | JTI | CTI |
|------|-----|-----|-----|
| 查询性能 | ⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐ |
| 数据库复杂度 | ⭐⭐⭐ | ⭐⭐ | ⭐ |
| 类型安全 | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ |
| 扩展性 | ⭐⭐ | ⭐⭐⭐ | ⭐⭐ |
| 存储效率 | ⭐⭐ | ⭐⭐⭐ | ⭐ |

**选择 STI 的原因**：当前场景下，子类特有字段较少（< 10 个），且查询性能是首要考虑因素。

## 实现细节

### 基类 MediaItem

```python
class MediaItem(Base):
    __tablename__ = "MediaItems"
    
    # STI 配置
    __mapper_args__ = {
        "polymorphic_on": "Type",  # 类型标识字段
        "polymorphic_identity": None,  # 基类无对应类型
        "with_polymorphic": "*",  # 查询时自动加载所有子类
    }
    
    # 公共字段
    Id = Column(Integer, primary_key=True)
    Type = Column(Enum(MediaType), nullable=False)
    Name = Column(String(500))
    Overview = Column(Text)
    # ... 其他公共字段
    
    # 子类特有字段（可为 NULL）
    ProductionYear = Column(Integer)  # Movie
    RunTimeTicks = Column(BigInteger)  # Movie/Episode
    SeasonCount = Column(Integer)  # Series
    # ... 其他子类字段
```

### 子类实现

每个子类通过 `polymorphic_identity` 标识自己的类型：

```python
class Movie(MediaItem):
    __mapper_args__ = {
        "polymorphic_identity": MediaType.Movie,
    }
    
    def get_duration_str(self) -> Optional[str]:
        """获取时长字符串"""
        if self.RunTimeTicks is None:
            return None
        total_seconds = self.RunTimeTicks / 10_000_000
        hours = int(total_seconds // 3600)
        minutes = int((total_seconds % 3600) // 60)
        if hours > 0:
            return f"{hours}h {minutes}m"
        return f"{minutes}m"
    
    def get_profit(self) -> Optional[float]:
        """计算利润"""
        if self.Revenue is None or self.Budget is None:
            return None
        return self.Revenue - self.Budget
```

### 类型转换机制

SQLAlchemy 自动处理类型转换：

```python
# 创建电影
movie = Movie(name="Test Movie", production_year=2024)
session.add(movie)
await session.flush()

# 查询时自动实例化为 Movie 类型
result = await session.execute(select(MediaItem).where(MediaItem.Id == movie.Id))
item = result.scalar_one()

# isinstance 检查
assert isinstance(item, Movie)  # True
assert isinstance(item, MediaItem)  # True
assert not isinstance(item, Series)  # True
```

## 子类列表

| 类型 | 类名 | 特有字段 | 特有方法 |
|------|------|----------|----------|
| Movie | Movie | ProductionYear, RunTimeTicks, Budget, Revenue | get_duration_str, get_profit, is_profitable |
| Series | Series | SeasonCount, EpisodeCount | get_duration_str, get_average_episodes_per_season |
| Season | Season | SeasonNumber | get_duration_str |
| Episode | Episode | EpisodeNumber | get_duration_str |
| Person | Person | BirthDate, DeathDate, BirthPlace | get_age, is_alive |
| Genre | Genre | GenreName | get_display_name |
| Studio | Studio | StudioName | get_display_name |
| Label | Label | LabelName | get_display_name |
| BoxSet | BoxSet | - | - |
| Source | Source | - | - |

## 优势

1. **查询性能**：单表查询，无需 JOIN，适合高频读取场景
2. **代码组织**：每种类型有独立类，包含特有逻辑
3. **类型安全**：Python 层面自动实例化正确类型
4. **简单易懂**：数据库结构简单，易于维护
5. **向后兼容**：现有代码无需修改即可继续工作

## 潜在限制

1. **表宽度**：子类特有字段会增加表宽度，可能影响性能
2. **NULL 值**：非对应类型的字段为 NULL，浪费存储空间
3. **扩展性**：新增子类需要修改表结构（添加列）
4. **查询复杂度**：按子类特有字段查询时需要类型过滤

## 最佳实践

1. **字段命名**：子类特有字段使用前缀或后缀区分（如 `Movie_Budget`）
2. **索引设计**：为常用查询字段创建索引
3. **查询优化**：使用 `select(MediaItem)` 查询所有类型，或使用具体类型查询
4. **类型检查**：使用 `isinstance()` 检查对象类型

## 示例代码

### 创建不同类型的实体

```python
# 电影
movie = Movie(
    name="星际穿越",
    production_year=2014,
    run_time_ticks=97200000000,  # 2h 42m
    budget=165000000.0,
    revenue=675120012.0,
)

# 剧集
series = Series(
    name="权力的游戏",
    season_count=8,
    episode_count=73,
)

# 人物
person = Person(
    name="克里斯托弗·诺兰",
    birth_date=datetime(1970, 7, 30, tzinfo=timezone.utc),
    birth_place="伦敦",
)
```

### 查询和使用

```python
# 查询所有媒体项
result = await session.execute(select(MediaItem))
items = result.scalars().all()

for item in items:
    print(f"{type(item).__name__}: {item.Name}")
    
    # 使用子类特有方法
    if isinstance(item, Movie):
        print(f"  时长: {item.get_duration_str()}")
        print(f"  利润: {item.get_profit()}")
    elif isinstance(item, Series):
        print(f"  季数: {item.SeasonCount}")
        print(f"  平均每季集数: {item.get_average_episodes_per_season()}")
    elif isinstance(item, Person):
        print(f"  年龄: {item.get_age()}")
        print(f"  是否在世: {item.is_alive()}")
```

## 测试覆盖

单元测试文件：`tests/test_sti.py`

测试内容：
- 类型转换：验证查询返回正确类型
- 方法调用：验证子类特有方法正确工作
- 继承关系：验证 isinstance 检查
- 字段访问：验证基类和子类字段可访问
- 关联关系：验证子类间的关联关系

## 迁移指南

### 从旧架构迁移

1. 运行 Alembic 迁移添加子类特有字段
2. 更新代码使用新的子类
3. 运行测试验证功能正确

### 新增子类

1. 在 `enums.py` 中添加新的 MediaType 枚举值
2. 在 `media_item.py` 中创建新的子类
3. 更新 `__init__.py` 导出新类
4. 创建 Alembic 迁移添加特有字段
5. 编写单元测试

## 性能考虑

1. **查询优化**：使用 `select(MediaItem)` 查询所有类型，避免多次查询
2. **索引设计**：为 `Type` 字段创建索引，加速类型过滤
3. **延迟加载**：使用 `deferred()` 延迟加载不常用的字段
4. **批量操作**：使用批量插入/更新提高性能

## 总结

单表继承（STI）是本项目的最佳选择，它提供了最优的查询性能和简单的实现。通过合理的设计和测试，可以构建一个类型安全、易于维护的媒体管理系统。
