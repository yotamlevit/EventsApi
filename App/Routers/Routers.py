from fastapi import FastAPI
from Events import events_api
from Users import users_api


def initialize_routers(app: FastAPI) -> None:
    app.include_router(events_api)
    app.include_router(users_api)