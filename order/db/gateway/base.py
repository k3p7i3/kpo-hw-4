import datetime

from abc import ABC
from pydantic import BaseModel
from sqlalchemy import Column, Table
from sqlalchemy.sql import ClauseElement

from order.db import database


class BaseGateway(ABC):
    table: Table
    prim_key: Column
    base_model: type
    model: type

    async def insert(self, base_object: BaseModel) -> int:
        query = self.table.insert().values(base_object.dict())
        object_id: int = await database.execute(query)
        return object_id

    async def _update(
        self,
        object_id: int,
        updated_at_flag: bool = True,
        **fields,
    ) -> int | None:
        # postgres haven't 'on_update', so insert 'updated_at' column manually
        if updated_at_flag:
            fields['updated_at'] = datetime.datetime.now()

        query = (
            self.table
            .update()
            .where(self.prim_key == object_id)
            .values(**fields)
            .returning(self.prim_key)
        )
        return await database.execute(query)

    async def update(self, object_id: int, base_object: BaseModel) -> int | None:
        object_update = base_object.dict(exclude_unset=True)
        if object_update:
            return await self._update(object_id, **object_update)

    async def get_one_by_cond(self, where_clause: ClauseElement):
        query: ClauseElement = self.table.select().where(where_clause)
        data = await database.fetch_one(query)
        if data:
            return self.model(**data._mapping)

    async def get_one(self, object_id: int):
        return await self.get_one_by_cond(self.prim_key == object_id)
