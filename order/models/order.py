from datetime import datetime
from enum import Enum
from pydantic import BaseModel, validator

from order.models.order_dish import OrderDishCreate, FullOrderDish


class OrderStatus(str, Enum):
    waiting = 'waiting'
    in_process = 'in_process'
    cancelled = 'cancelled'
    executed = 'executed'


class OrderBase(BaseModel):
    user_id: int
    status: OrderStatus = OrderStatus.waiting
    special_requests: str | None = None


class Order(OrderBase):
    order_id: int
    created_at: datetime
    updated_at: datetime


class OrderCreate(OrderBase):
    dishes: list[OrderDishCreate]

    @validator('dishes')
    def dishes_not_empty(cls, v):
        if not v:
            raise ValueError('Order has no dishes')
        return v

    @validator('dishes', each_item=True)
    def check_dish_quantity(cls, v):
        if v.quantity <= 0:
            raise ValueError('Dish quantity must be positive number')
        return v


class FullOrder(Order):
    dishes: list[FullOrderDish]
