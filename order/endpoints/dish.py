from fastapi import APIRouter, Depends

from order.endpoints.permissions import only_manager
from order.logic import DishHandler
from order.models import Dish, DishBase


router = APIRouter(prefix='/dish', tags=['dish'])


@router.post(
    path='/create',
    status_code=201,
    dependencies=[Depends(only_manager)],
)
async def create_dish(dish: DishBase):
    logic_handler: DishHandler = DishHandler()
    dish_id: int = await logic_handler.create_dish(dish)
    return {'dish_id': dish_id}


@router.get(
    path='/{dish_id}',
    response_model=Dish,
    dependencies=[Depends(only_manager)],
)
async def get_dish(dish_id: int):
    logic_handler: DishHandler = DishHandler()
    dish: Dish = await logic_handler.get_dish(dish_id)
    return dish


@router.patch(
    path='/{dish_id}',
    dependencies=[Depends(only_manager)],
)
async def update_dish(dish_id: int, dish: DishBase):
    logic_handler: DishHandler = DishHandler()
    await logic_handler.update_dish(dish_id=dish_id, dish=dish)


@router.delete(
    path='/{dish_id}',
    dependencies=[Depends(only_manager)],
)
async def delete_dish(dish_id: int):
    logic_handler: DishHandler = DishHandler()
    await logic_handler.delete_dish(dish_id)
