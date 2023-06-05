from sqlalchemy.sql import ClauseElement

from auth.db import database, session_table
from auth.models import Session, SessionBase


class SessionGateway:
    table = session_table

    async def create_session(self, session: SessionBase) -> int:
        query: ClauseElement = self.table.insert().values(session.dict())
        session_id: int = await database.execute(query)
        return session_id

    async def _get_session_by_cond(self, condition: ClauseElement):
        query: ClauseElement = self.table.select().where(condition)
        data = await database.fetch_one(query)
        if data:
            return Session(**data._mapping)

    async def get_session_by_token(self, token: str) -> Session:
        where_clause: ClauseElement = self.table.c.session_token == token
        return await self._get_session_by_cond(where_clause)