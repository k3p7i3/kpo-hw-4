from sqlalchemy import select
from sqlalchemy.sql import and_

from order.db import database, dishes_table
from order.db.gateway.base import BaseGateway
from order.models import DishBase, Dish


class DishGateway(BaseGateway):
    table = dishes_table
    prim_key = dishes_table.c.dish_id
    base_model = DishBase
    model = Dish

    async def delete_dish(self, dish_id: int) -> int | None:
        # to keep store dish info in database, just mark it as unavailable
        query = (
            self.table
            .update()
            .where(self.prim_key == dish_id)
            .values(is_available=False)
        )
        return await database.execute(query)

    async def get_dish(self, dish_id: int) -> Dish | None:
        return await self.get_one(dish_id)

    async def get_available_dishes(self) -> list[Dish]:
        query = (
            self.table.select()
            .where(
                and_(
                    self.table.c.is_available.is_(True),
                    self.table.c.quantity > 0,
                )
            )
        )
        rows = await database.fetch_all(query)
        dishes = [self.model(**row._mapping) for row in rows]
        return dishes

    async def get_price(self, dish_id: int) -> float:
        query = (
            select([self.table.c.price])
            .where(self.prim_key == dish_id)
        )
        row = await database.fetch_one(query)
        return row.price

    async def update_quantity(self, dish_id: int, quantity: int):
        await self._update(object_id=dish_id, quantity=quantity)
