from order.db import database, orders_table
from order.db.gateway.base import BaseGateway
from order.db.gateway.order_dish import OrderDishGateway
from order.models import (
    Order,
    OrderBase,
    OrderCreate,
    OrderStatus,
    FullOrder,
)


class OrderGateway(BaseGateway):
    table = orders_table
    prim_key = orders_table.c.order_id
    base_model = OrderBase
    model = Order
    dishes_gateway = OrderDishGateway()

    async def get_order(self, order_id: int) -> Order:
        return await self.get_one(order_id)

    async def get_full_order(self, order_id: int) -> FullOrder | None:
        order: Order = await self.get_order(order_id)
        if not order:
            return
        dishes = await self.dishes_gateway.get_full_order_dishes(order_id)
        full_order: FullOrder = FullOrder(**order.dict(), dishes=dishes)
        return full_order

    async def create_order(self, order: OrderCreate) -> int:
        order_data = order.dict()
        order_data.pop('dishes')
        base_order: OrderBase = OrderBase(**order_data)
        order_id = await self.insert(base_order)
        await self.dishes_gateway.create_dishes_for_order(
            order_id=order_id,
            order_dishes=order.dishes,
        )
        return order_id

    async def update_status(self, order_id: int, status: OrderStatus) -> int | None:
        return await self._update(object_id=order_id, status=status)
