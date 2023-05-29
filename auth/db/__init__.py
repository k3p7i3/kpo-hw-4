import databases
from .tables import metadata, user_table, session_table


database = databases.Database(url)


async def open_db():
    # connect to database
    await database.connect()


async def close_db():
    # disconnect from database
    await database.disconnect()
