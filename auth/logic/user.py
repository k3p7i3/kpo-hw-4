from fastapi import HTTPException

from auth.db.gateway import UserGateway, SessionGateway
from auth.models import (
    Session,
    User,
    UserAuth,
    UserRegistrate,
)


class UserLogic:
    def __init__(self):
        self.db_users = UserGateway()
        self.db_sessions = SessionGateway()

    async def _does_username_exist(self, username: str) -> bool:
        user: User = await self.db_users.get_user_by_username(username)
        return user is not None

    async def _does_email_exist(self, email: str) -> bool:
        user: User = await self.db_users.get_user_by_email(email)
        return user is not None

    async def create_user(self, user: UserRegistrate) -> int:
        user_id: int = await self.db_users.create_user(user)

        if not user_id:
            # try to identify error if possible and raise it
            if await self._does_username_exist(user.username):
                raise HTTPException(status_code=400, detail='User with this username already exist')
            if await self._does_email_exist(user.email):
                raise HTTPException(status_code=400, detail='User with this email already exist')
            raise HTTPException(status_code=500, detail='Registration failed')

        return user_id

    async def identify_user_by_login(self, user: UserAuth) -> int:
        user: User = await self.db_users.get_user_by_auth(auth_user=user)
        if not user:
            raise HTTPException(status_code=400, detail='Wrong email or password')
        return user.user_id


