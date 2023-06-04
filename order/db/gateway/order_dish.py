from sqlalchemy import select

from order.db import database, dishes_table, order_dishes_table
from order.db.gateway.base import BaseGateway
from order.db.gateway.dish import DishGateway
from order.models import (
    OrderDishCreate,
    OrderDishBase,
    OrderDish,
    FullOrderDish,
)


class OrderDishGateway(BaseGateway):
    table = order_dishes_table
    prim_key = order_dishes_table.c.order_dish_id
    base_model = OrderDishBase
    model = OrderDish
    dish_gateway = DishGateway()

    async def get_order_dish(self, order_dish_id: int) -> OrderDish:
        return await self.get_one(order_dish_id)

    async def get_full_order_dish(self, order_dish_id: int) -> FullOrderDish:
        query = (
            select([
                self.table,
                dishes_table.c.name,
                dishes_table.c.description,
            ])
            .select_from(self.table.join(dishes_table))
            .where(self.prim_key == order_dish_id)
        )
        data = await database.fetch_one(query)
        if data:
            return FullOrderDish(**data._mapping)

    async def get_full_order_dishes(self, order_id: int) -> [FullOrderDish]:
        query = (
            select([
                self.table,
                dishes_table.c.name,
                dishes_table.c.description,
            ])
            .select_from(self.table.join(dishes_table))
            .where(self.table.order_id == order_id)
        )
        data = await database.fetch_one(query)
        if data:
            return FullOrderDish(**data._mapping)

        rows = await database.fetch_all(query)
        order_dishes = []
        for row in rows:
            order_dishes.append(FullOrderDish(**row._mapping))
        return order_dishes

    async def fulfill_order_dishes(
        self,
        order_id: int,
        order_dishes: [OrderDishCreate],
    ) -> [OrderDishBase]:
        base_dishes: [OrderDishBase] = []
        for order_dish in order_dishes:
            price = await self.dish_gateway.get_price(order_dish.dish_id)
            order_dish_base: OrderDishBase = OrderDishBase(
                order_id=order_id,
                price=price,
                **order_dish.dict(),
            )
            base_dishes.append(order_dish_base)
        return base_dishes

    async def create_order_dishes(self, order_dishes: [OrderDishBase]):
        query = self.table.insert()
        values = [order_dish.dict() for order_dish in order_dishes]
        await database.execute_many(query, values)

    async def create_dishes_for_order(
        self,
        order_id: int,
        order_dishes: [OrderDishCreate],
    ):
        fulfilled_dishes = await self.fulfill_order_dishes(
            order_id=order_id,
            order_dishes=order_dishes,
        )
        if fulfilled_dishes:
            await self.create_order_dishes(order_dishes=fulfilled_dishes)
