# coding: utf-8
"""
Base Model - 基础模型类
========================

SQLAlchemy 声明式基类，所有模型类都继承自此类。
提供命名约束等最佳实践配置。

命名约束规则：
- ix: 索引前缀
- uq: 唯一约束前缀
- ck: 检查约束前缀
- fk: 外键约束前缀
- pk: 主键约束前缀

作者：白鸟青城
版本：3.0.0 (简化注释)
"""

from sqlalchemy import MetaData
from sqlalchemy.orm import declarative_base


NAMING_CONVENTION = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}


metadata = MetaData(naming_convention=NAMING_CONVENTION)

Base = declarative_base(metadata=metadata)
