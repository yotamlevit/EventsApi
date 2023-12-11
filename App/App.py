from fastapi import FastAPI
from Routes import initialize_routers


def app() -> FastAPI:
    app = FastAPI()
    initialize_routers(app)
    return app