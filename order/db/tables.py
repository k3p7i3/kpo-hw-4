from sqlalchemy import (
    Column,
    ForeignKey,
    MetaData,
    Table,
    types,
)
from sqlalchemy.sql import func

from order.models import OrderStatus

metadata = MetaData()

dishes_table = Table(
    'dish',
    metadata,
    Column('dish_id', types.Integer, primary_key=True),
    Column('name', types.String(128), nullable=False),
    Column('description', types.Text),
    Column('price', types.Float(2), nullable=False),
    Column('quantity', types.Integer, nullable=False),
    Column('is_available', types.Boolean, nullable=False, default=True),
    Column('created_at', types.DateTime, nullable=False, server_default=func.now()),
    Column('updated_at', types.DateTime, nullable=False, onupdate=func.now()),
)


orders_table = Table(
    'order',
    metadata,
    Column('order_id', types.Integer, primary_key=True),
    Column('user_id', types.Integer, nullable=False),
    Column('status', types.Enum(OrderStatus), nullable=False),
    Column('special_requests', types.Text),
    Column('created_at', types.DateTime, nullable=False, server_default=func.now()),
    Column('updated_at', types.DateTime, nullable=False, onupdate=func.now()),
)


order_dishes_table = Table(
    'order_dish',
    metadata,
    Column('order_dish_id', types.Integer, primary_key=True),
    Column('order_id', ForeignKey('order.order_id'), nullable=False),
    Column('dish_id', ForeignKey('dish.dish_id'), nullable=False),
    Column('quantity', types.Integer, nullable=False),
    Column('price', types.Float(2), nullable=False),
)
