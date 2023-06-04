from fastapi import FastAPI

import db
from endpoints import dish_router, menu_router, order_router


def bind_events(app):
    @app.on_event('startup')
    async def startup():
        await db.open_db()

    @app.on_event('shutdown')
    async def shutdown():
        await db.close_db()


def get_app():
    app = FastAPI(title='OrderApp')
    app.include_router(order_router)
    app.include_router(dish_router)
    app.include_router(menu_router)
    bind_events(app)
    return app


app = get_app()
