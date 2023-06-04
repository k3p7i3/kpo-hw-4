from fastapi import HTTPException

from order.db.gateway import DishGateway
from order.models import Dish, DishBase


class DishHandler:
    def __init__(self):
        self.dish_gateway = DishGateway()

    async def get_menu(self) -> [Dish]:
        dishes = await self.dish_gateway.get_available_dishes()
        return dishes

    def _check_dish_for_creation(self, dish: DishBase):
        if not dish.name:
            raise HTTPException(status_code=422, detail='Dish name can\'t be empty')
        if dish.quantity is None:
            raise HTTPException(status_code=422, detail='Dish quantity can\'t be null')
        if dish.price is None:
            raise HTTPException(status_code=422, detail='Dish price can\'t be null')

    async def create_dish(self, dish: DishBase) -> int:
        self._check_dish_for_creation(dish)
        dish_id = await self.dish_gateway.insert(dish)
        if not dish_id:
            raise HTTPException(status_code=500, detail='Couldn\'t create new dish')
        return dish_id

    async def get_dish(self, dish_id: int) -> Dish:
        dish = await self.dish_gateway.get_dish(dish_id)
        if not dish:
            raise HTTPException(
                status_code=500,
                detail='Couldn\'t get the dish, perhaps the dish doesn\'t exist',
            )
        return dish

    async def update_dish(self, dish_id: int, dish: DishBase):
        updated_dish_id = await self.dish_gateway.update(dish_id, dish)
        if not updated_dish_id:
            raise HTTPException(
                status_code=500,
                detail='Couldn\'t update the dish, perhaps the dish doesn\'t exist',
            )

    async def delete_dish(self, dish_id):
        deleted_dish_id = await self.dish_gateway.delete_dish(dish_id)
        if not deleted_dish_id:
            raise HTTPException(
                status_code=500,
                detail='Couldn\'t delete the dish',
            )
