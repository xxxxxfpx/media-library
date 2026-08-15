# 配置文件说明

后端配置采用「默认配置 + 本地覆盖 + 密钥合并」三级机制：

| 文件 | 作用 | 是否提交 |
|------|------|----------|
| `config/default.yaml` | 生产默认配置（非敏感） | ✅ 提交 |
| `config/setting.yaml` | UI 卡牌显示配置 | ✅ 提交 |
| `config/local.yaml` | 本地开发覆盖（复制自 `local.example.yaml`） | ❌ gitignore |
| `env.yaml` | 开发/测试专用配置 | ✅ 提交 |
| `secrets/config.yaml` | 云盘/远程库等敏感凭据（复制自 `config.example.yaml`） | ❌ gitignore |

## 加载顺序

1. `CONFIG_PATH` 环境变量指定的文件（优先级最高）
2. `ENV=development` 时使用 `env.yaml`
3. `config/local.yaml`（若存在）
4. `config/default.yaml`（兜底）

加载后，`secrets/config.yaml`（或 `SECRETS_PATH` 指向的文件）中的同名字段会覆盖默认值。
