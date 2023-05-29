from sqlalchemy import and_
from sqlalchemy.sql import ClauseElement

from auth.db import database, user_table
from auth.models import UserRegistrate, User, UserAuth


class UserGateway:
    # contains logic of interaction with database in terms of user entity
    table = user_table

    async def create_user(self, user: UserRegistrate) -> int:
        query: ClauseElement = self.table.insert().values(user.dict())
        user_id: int = await database.execute(query)
        return user_id

    async def _get_user_by_condition(self, condition: ClauseElement) -> User | None:
        query: ClauseElement = self.table.select().where(condition)
        data = await database.fetch_one(query)
        if data:
            return User(**data._mapping)

    async def get_user_by_auth(self, auth_user: UserAuth) -> User | None:
        where_clause: ClauseElement = and_(
            self.table.email == auth_user.email,
            self.table.password_hash == auth_user.password_hash,
        )
        return await self._get_user_by_condition(where_clause)

    async def get_user(self, user_id: int) -> User | None:
        where_clause: ClauseElement = (self.table.c.user_id == user_id)
        return await self._get_user_by_condition(where_clause)

    async def get_user_by_username(self, username: str) -> User | None:
        where_clause: ClauseElement = (self.table.c.username.is_(username))
        return await self._get_user_by_condition(where_clause)

    async def get_user_by_email(self, email: str) -> User | None:
        where_clause: ClauseElement = (self.table.c.email.is_(email))
        return await self._get_user_by_condition(where_clause)
