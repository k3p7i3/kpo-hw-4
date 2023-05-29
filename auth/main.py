from fastapi import FastAPI

import db
from src.routers import api_router


def bind_events(app):
    @app.on_event('startup')
    async def startup():
        await db.open_db()

    @app.on_event('shutdown')
    async def shutdown():
        await db.close_db()


def get_app():
    app = FastAPI(title='AuthApp')
    app.include_router(api_router, prefix='/api')
    bind_events(app)
    return app


app = get_app()