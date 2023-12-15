from fastapi import FastAPI, Depends
from .Routers import initialize_routers
from .Dependencies import authentication
from slowapi.errors import RateLimitExceeded
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.middleware import SlowAPIMiddleware

tags_metadata = [
    {
        "name": "Event API",
        "description": "All Event related operations",
    },
    {
        "name": "Users API",
        "description": "All Users related operations",
    },
]


description = """
RalfaBet Backend API 🔥🔥🔥

## Items

You can **read items**.

## For Users

You will be able to:

### Events:
* **Get all events**
* **Get a specific event**
* **Create a new event**
* **Update an existing event**
* **Delete an event**

### Users
* **Create users** (_not implemented_).
* **Read users** (_not implemented_).
"""

def app() -> FastAPI:
    app = FastAPI(description=description, openapi_tags=tags_metadata, dependencies=[Depends(authentication)])
    limiter = Limiter(key_func=get_remote_address, default_limits=["5/5seconds"])
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
    app.add_middleware(SlowAPIMiddleware)
    initialize_routers(app)
    return app