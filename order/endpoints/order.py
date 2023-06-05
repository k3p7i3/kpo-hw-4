from fastapi import APIRouter, BackgroundTasks, Depends

from order.endpoints.permissions import (
    only_authorized,
    access_to_order,
)
from order.models import FullOrder, OrderCreate
from order.logic import OrderHandler, process_order


router = APIRouter(prefix='/orders', tags=['order'])


@router.post(
    path='/create',
    status_code=201,
    dependencies=[Depends(only_authorized)],
)
async def create_order(order: OrderCreate, background_tasks: BackgroundTasks):
    logic_handler = OrderHandler()
    order_id: int = await logic_handler.create_order(order)
    background_tasks.add_task(process_order, order_id)
    return {'order_id': order_id}


@router.get(
    path='/{order_id}',
    response_model=FullOrder,
    dependencies=[Depends(access_to_order)],
)
async def read_order(order_id: int):
    logic_handler = OrderHandler()
    order: FullOrder = await logic_handler.get_order(order_id)
    return order


@router.post(
    path='/{order_id}/cancel',
    status_code=200,
    dependencies=[Depends(access_to_order)],
)
async def cancel_order(order_id: int):
    logic_handler = OrderHandler()
    await logic_handler.cancel_order(order_id)
