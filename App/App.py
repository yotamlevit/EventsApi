from fastapi import FastAPI, Depends
from .Routers import initialize_routers
from .Dependencies import authenticate, bl_factory


def app() -> FastAPI:
    app = FastAPI(dependencies=[Depends(authenticate)])
    initialize_routers(app)
    return app