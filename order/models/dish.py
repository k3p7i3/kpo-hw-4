from datetime import datetime
from pydantic import BaseModel, validator


class DishBase(BaseModel):
    name: str = None
    description: str | None = None
    price: float = None
    quantity: int = None
    is_available: bool = True

    @validator('price', 'quantity')
    def negative_number_check(cls, v):
        if v is not None and v < 0:
            raise ValueError('Price or quantity can\'t be a negative number')
        return v


class Dish(DishBase):
    dish_id: int
    created_at: datetime = None
    updated_at: datetime = None
