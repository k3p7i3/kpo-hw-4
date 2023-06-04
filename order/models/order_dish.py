from pydantic import BaseModel


class OrderDishCreate(BaseModel):
    dish_id: int
    quantity: int


class OrderDishBase(OrderDishCreate):
    order_id: int = None
    price: float


class OrderDish(OrderDishBase):
    order_dish_id: int


class FullOrderDish(OrderDish):
    name: str
    description: str | None = None
