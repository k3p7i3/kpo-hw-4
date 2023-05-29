from sqlalchemy import (
    Column,
    ForeignKey,
    MetaData,
    Table,
    types,
)
from sqlalchemy.sql import func

from auth.models import UserRole

metadata = MetaData()


# declaration of 'user' table in code
user_table = Table(
    'user',
    metadata,
    Column('user_id', types.Integer, primary_key=True),
    Column('username', types.String(50), nullable=False, unique=True),
    Column('email', types.String(100), nullable=False, unique=True),
    Column('password_hash', types.String(256), nullable=False),
    Column('role', types.Enum(UserRole), nullable=False),
    Column('created_at', types.DateTime, nullable=False, server_default=func.now()),
    Column('updated_at', types.DateTime, nullable=False, onupdate=func.now()),
)


# declaration of 'session' table in code
session_table = Table(
    'session',
    metadata,
    Column('session_id', types.Integer, primary_key=True),
    Column('user_id', ForeignKey('user.user_id'), nullable=False),
    Column('session_token', types.String(512), nullable=False),
    Column('expires_at', types.DateTime, nullable=False),
)
