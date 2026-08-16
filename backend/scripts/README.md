# backend/scripts 脚本说明

按职责划分的运维/数据脚本目录。**多数为一次性脚本，运行前请先阅读本文件与脚本内注释。**

## 目录分类

| 目录 | 用途 | 注意事项 |
|------|------|----------|
| `checks/` | 数据校验类脚本（`check_*.py`） | 只读为主，用于排查数据问题 |
| `migrations/` | 数据库结构/数据迁移脚本（`migrate_*.py`、`add_*_column.py`、`remove_*_column.py` 等） | **执行前备份数据库**；部分脚本针对特定历史数据（如 3102 系列） |
| `tools/` | 维护与验证工具（`fix_*.py`、`sync_metadata.py`、`test_*.py`、`analyze_*.py` 等） | `test_*.py` 为手工冒烟/回归脚本，非 pytest 测试；`test_api*` 为 API 冒烟脚本 |
| `legacy/` | **历史一次性脚本存档** | **标记为不可直接运行**：引用旧 ORM 模型（如 `ItemLinks.Type`、`ItemLinkType`、`OriginalTitle` 等已删除字段），运行即崩溃，仅保留作为迁移历史参考 |

## 运行约定

- 涉及远程数据库的脚本凭据通过环境变量读取（`REMOTE_DB_HOST/PORT/NAME/USER/PASSWORD`），未设置则失败退出；**不得硬编码凭据**。
- 涉及远程数据源的脚本：先确认源可用，再运行。
- 脚本运行时的工作目录应为 `backend/`（保证 `app`、`database`、`config` 等包可被导入）。
