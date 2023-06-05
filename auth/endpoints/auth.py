from fastapi import APIRouter, Header

from auth.logic import UserLogic
from auth.models import (
    Token,
    UserAuth,
    UserInfo,
    UserRegistrate,
)


router = APIRouter()


@router.post(
    path='/registration',
    status_code=201,
    response_model=Token,
)
async def registrate_user(user: UserRegistrate):
    logic_handler: UserLogic = UserLogic()
    token = await logic_handler.registrate_user(user)
    return Token(session_token=token)


@router.post(
    path='/auth',
    status_code=201,
    response_model=Token,
)
async def auth_user(user: UserAuth):
    logic_handler: UserLogic = UserLogic()
    token = await logic_handler.login_user(user)
    return Token(session_token=token)


@router.get(
    path='/info',
    status_code=200,
    response_model=UserInfo,
)
async def get_user_info(x_token: str = Header(...)):
    logic_handler: UserLogic = UserLogic()
    return await logic_handler.get_user_info_by_token(x_token)
