from fastapi import APIRouter

from order.logic.dish import DishHandler
from order.models import Dish


router = APIRouter(prefix='/menu', tags=['menu'])


@router.get(
    path='',
    response_model=list[Dish],
)
async def get_menu() -> list[Dish]:
    logic_handler: DishHandler = DishHandler()
    menu: list[Dish] = await logic_handler.get_menu()
    return menu
