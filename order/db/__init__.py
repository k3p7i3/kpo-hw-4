import databases

from order.config import settings
from .tables import (
    metadata,
    dishes_table,
    orders_table,
    order_dishes_table,
)


database = databases.Database(settings.database_url)


async def open_db():
    # connect to database
    await database.connect()


async def close_db():
    # disconnect from database
    await database.disconnect()
