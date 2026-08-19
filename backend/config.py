"""
配置加载模块
"""

import os
import sys
import base64
import yaml
from dataclasses import dataclass
from typing import Optional


@dataclass
class DatabaseConfig:
    type: str = "sqlite"
    sqlite_path: str = "./data/database/media.db"
    host: str = "localhost"
    port: int = 5432
    database: str = "media_db"
    username: str = "postgres"
    password: str = ""

    @property
    def url(self) -> str:
        if self.type == "sqlite":
            return f"sqlite:///{self.sqlite_path}"
        return f"postgresql://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}"


@dataclass
class AppConfig:
    name: str = "Media Management System"
    version: str = "1.0.0"
    debug: bool = True
    secret_key: str = ""
    admin_username: str = "admin"
    admin_password: str = ""
    disk_path: str = "C:\\" if sys.platform == "win32" else "/"
    host: str = "0.0.0.0"
    port: int = 8000


@dataclass
class JWTConfig:
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7


@dataclass
class CloudAuthConfig:
    username: str = ""
    password: str = ""
    prefix: str = ""

    @property
    def basic_auth_token(self) -> str:
        token = base64.b64encode(f"{self.username}:{self.password}".encode()).decode()
        return token


@dataclass
class LoggingConfig:
    level: Optional[str] = None
    file_enabled: bool = True
    file_path: str = "data/log/app.log"
    rotate_max_bytes: int = 50 * 1024 * 1024
    backup_count: int = 3


def _merge_secret_config(data: dict) -> dict:
    """Merge local secrets over the selected non-sensitive config."""
    secrets_path = os.environ.get(
        "SECRETS_PATH",
        os.path.join(os.path.dirname(os.path.dirname(__file__)), "secrets", "config.yaml"),
    )
    if not os.path.exists(secrets_path):
        return data

    with open(secrets_path, "r", encoding="utf-8") as f:
        secrets = yaml.safe_load(f) or {}

    for section, values in secrets.items():
        if isinstance(values, dict):
            data.setdefault(section, {}).update(values)
        else:
            data[section] = values
    return data


class Config:
    def __init__(self, config_path: Optional[str] = None):
        self.config_path = config_path or self._find_config_file()
        self.database = DatabaseConfig()
        self.app = AppConfig()
        self.jwt = JWTConfig()
        self.cloud_auth = CloudAuthConfig()
        self.logging = LoggingConfig()
        self.remote_database = {}
        self._load_config()

    def _find_config_file(self) -> str:
        # 优先使用环境变量指定的配置文件
        if os.environ.get('CONFIG_PATH'):
            return os.environ['CONFIG_PATH']
        # 开发环境使用 env.yaml
        if os.environ.get('ENV') == 'development' and os.path.exists('env.yaml'):
            return 'env.yaml'
        # 配置文件目录（相对本模块所在位置，与运行目录无关）
        config_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config")
        possible_paths = [
            "config.yaml",
            "./config.yaml",
            os.path.join(config_dir, "local.yaml"),
            os.path.join(config_dir, "default.yaml"),
        ]
        for path in possible_paths:
            if os.path.exists(path):
                return path
        return os.path.join(config_dir, "default.yaml")

    def _load_config(self):
        data = {}
        if not os.path.exists(self.config_path):
            print(f"配置文件 {self.config_path} 不存在，使用默认配置")
        else:
            try:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    data = yaml.safe_load(f) or {}
            except Exception as e:
                print(f"加载配置文件失败: {e}，使用默认配置")

        # 始终合并 secrets 覆盖：即使主配置文件缺失（如容器内 CONFIG_PATH
        # 指向不存在的 local.yaml），secrets/config.yaml 中的密钥也必须生效，
        # 否则启动守卫会因 secret_key 为空而拒绝启动
        data = _merge_secret_config(data)
        if not data:
            return

        try:

            if 'database' in data:
                db = data['database']
                self.database = DatabaseConfig(
                    type=db.get('type', self.database.type),
                    sqlite_path=db.get('sqlite_path', self.database.sqlite_path),
                    host=db.get('host', self.database.host),
                    port=db.get('port', self.database.port),
                    database=db.get('database', self.database.database),
                    username=db.get('username', self.database.username),
                    password=db.get('password', self.database.password),
                )

            if 'app' in data:
                app = data['app']
                self.app = AppConfig(
                    name=app.get('name', self.app.name),
                    version=app.get('version', self.app.version),
                    debug=app.get('debug', self.app.debug),
                    secret_key=app.get('secret_key', self.app.secret_key),
                    admin_username=app.get('admin', {}).get('username', self.app.admin_username),
                    admin_password=app.get('admin', {}).get('password', self.app.admin_password),
                    disk_path=app.get('disk_path', self.app.disk_path),
                    host=app.get('host', self.app.host),
                    port=app.get('port', self.app.port),
                )

            if 'jwt' in data:
                jwt = data['jwt']
                self.jwt = JWTConfig(
                    algorithm=jwt.get('algorithm', self.jwt.algorithm),
                    access_token_expire_minutes=jwt.get('access_token_expire_minutes', self.jwt.access_token_expire_minutes),
                    refresh_token_expire_days=jwt.get('refresh_token_expire_days', self.jwt.refresh_token_expire_days),
                )

            if 'cloud_auth' in data:
                ca = data['cloud_auth']
                self.cloud_auth = CloudAuthConfig(
                    username=ca.get('username', self.cloud_auth.username),
                    password=ca.get('password', self.cloud_auth.password),
                    prefix=ca.get('prefix', self.cloud_auth.prefix),
                )

            if 'logging' in data:
                lg = data['logging']
                self.logging = LoggingConfig(
                    level=lg.get('level') or None,
                    file_enabled=lg.get('file_enabled', self.logging.file_enabled),
                    file_path=lg.get('file_path', self.logging.file_path),
                    rotate_max_bytes=lg.get('rotate_max_bytes', self.logging.rotate_max_bytes),
                    backup_count=lg.get('backup_count', self.logging.backup_count),
                )

            if 'remote_database' in data:
                self.remote_database = data['remote_database']
        except Exception as e:
            print(f"加载配置文件失败: {e}，使用默认配置")


config = Config()


def get_config() -> Config:
    return config


def get_remote_db_config() -> dict:
    """Return the remote database connection settings from the secret file."""
    remote = getattr(config, "remote_database", None)
    if remote is None:
        raise RuntimeError("remote_database is not configured in secrets/config.yaml")
    return {
        "host": remote["host"],
        "port": remote.get("port", 5432),
        "database": remote["database"],
        "user": remote.get("username", remote.get("user")),
        "password": remote["password"],
    }
