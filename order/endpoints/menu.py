from fastapi import APIRouter

from order.logic.dish import DishHandler
from order.models import Dish


router = APIRouter(prefix='/menu', tags=['menu'])


@router.get(
    path='',
    response_model=[Dish],
)
async def get_menu():
    logic_handler: DishHandler = DishHandler()
    menu: [Dish] = await logic_handler.get_menu()
    return menu
