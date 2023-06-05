import time
from collections import defaultdict
from fastapi import HTTPException
from fastapi.concurrency import run_in_threadpool

from order.db.gateway import DishGateway, OrderGateway
from order.models import (
    Dish,
    FullOrder,
    Order,
    OrderCreate,
    OrderDishCreate,
    OrderStatus,
)


async def process_order(order_id: int):
    order_gateway: OrderGateway = OrderGateway()
    await order_gateway.update_status(
        order_id=order_id,
        status=OrderStatus.in_process,
    )
    await run_in_threadpool(lambda: time.sleep(45))
    order = await order_gateway.get_order(order_id)
    if order.status == OrderStatus.in_process:
        await order_gateway.update_status(
            order_id=order_id,
            status=OrderStatus.executed,
        )


class OrderHandler:
    def __init__(self):
        self.order_gateway = OrderGateway()
        self.dish_gateway = DishGateway()

    async def get_plain_order(self, order_id: int) -> Order:
        order = await self.order_gateway.get_order(order_id)
        if not order:
            raise HTTPException(status_code=404, detail='Order does not exist')
        return order

    async def get_order(self, order_id: int) -> FullOrder:
        order: FullOrder = await self.order_gateway.get_full_order(order_id)
        if not order:
            raise HTTPException(status_code=404, detail='Order does not exist')
        return order

    async def _update_dishes_quantity(self, dishes: dict[int, int]):
        # receive map of [dish_id, order
        for dish_id, dish_quantity in dishes.items():
            await self.dish_gateway.update_quantity(dish_id, dish_quantity)

    async def _check_and_update_dishes(self, dishes: list[OrderDishCreate]):
        #  construct map of [dish_id, dish quantity] to check that the whole order is available
        dish_map = defaultdict(int)
        for dish in dishes:
            dish_map[dish.dish_id] += dish.quantity

        error_dishes: list[int] = []
        updated_quantities = {}  # map of [dish_id, new quantity] for later update in db
        for dish_id, request_quantity in dish_map.items():
            db_dish: Dish = await self.dish_gateway.get_dish(dish_id)
            updated_quantities[dish_id] = db_dish.quantity - request_quantity
            if (not db_dish
                    or db_dish.quantity < request_quantity
                    or not db_dish.is_available):
                error_dishes.append(dish_id)

        if error_dishes:
            message: str = ('Impossible to order dishes: '
                            + ', '.join(map(str, error_dishes))
                            + '. Perhaps dish is unavailable or not in stock.')
            raise HTTPException(status_code=400, detail=message)

        await self._update_dishes_quantity(updated_quantities)

    async def create_order(self, order: OrderCreate) -> int:
        if order.status is not OrderStatus.waiting:
            raise HTTPException(status_code=422, detail='Impossible status of order')
        await self._check_and_update_dishes(dishes=order.dishes)
        order_id: int = await self.order_gateway.create_order(order=order)
        if not order_id:
            raise HTTPException(status_code=500, detail='Unable to create order')
        return order_id

    async def cancel_order(self, order_id: int):
        order: Order = await self.order_gateway.get_order(order_id)

        # handle all possible errors
        if not order:
            raise HTTPException(status_code=404, detail='Order does not exist')
        if order.status is OrderStatus.executed:
            raise HTTPException(status_code=409, detail='Unable to cancel already executed order')
        if order.status is OrderStatus.cancelled:
            raise HTTPException(status_code=409, detail='Unable to cancel already cancelled order')

        await self.order_gateway.update_status(order_id=order_id, status=OrderStatus.cancelled)
