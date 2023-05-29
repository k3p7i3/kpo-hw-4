from fastapi import APIRouter

router = APIRouter()


@router.post(path='/registration')
async def registrate_user():
    pass


@router.post(path='/auth')
async def auth_user():
    pass


@router.get(path='')
async def get_user_info():
    pass