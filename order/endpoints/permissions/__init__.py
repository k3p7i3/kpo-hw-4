from fastapi import Header, HTTPException
from order.lib.auth import AuthClient
from order.logic.order import OrderHandler

def _check_token_presence(x_token: str):
    if not x_token:
        raise HTTPException(
            status_code=401,
            detail='No token is provided',
        )


async def is_user(user_id: int, current_user: dict):
    return current_user.get('user_id') == user_id


async def is_manager(current_user: dict):
    return current_user.get('role') == 'manager'


async def is_chef(current_user: dict):
    return current_user.get('role') == 'chef'


async def only_authorized(x_token: str = Header()):
    _check_token_presence(x_token)

    user_info = await AuthClient().get_user_info(token=x_token)
    if not user_info.get('role'):
        raise HTTPException(
            status_code=401,
            detail='Empty user role',
        )


async def only_manager(x_token: str = Header()):
    _check_token_presence(x_token)

    user_info = await AuthClient().get_user_info(token=x_token)
    if not is_manager(user_info):
        raise HTTPException(
            status_code=403,
            detail='Only manager can change menu',
        )


async def user_private_info(user_id: int, x_token: str = Header()):
    _check_token_presence(x_token)

    user_info = await AuthClient().get_user_info(token=x_token)
    if not (
        is_user(user_id, user_info)
        or is_manager(user_info) or is_chef(user_info)
    ):
        raise HTTPException(
            status_code=403,
            detail='Only manager can change menu',
        )


async def access_to_order(order_id: int, x_token: str = Header()):
    order = await OrderHandler().get_plain_order(order_id=order_id)
    user_id = order.user_id
    await user_private_info(user_id=user_id, x_token=x_token)
