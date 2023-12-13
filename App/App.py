from fastapi import FastAPI, Depends
from .Routers import initialize_routers
from .Dependencies import authenticate, bl_factory


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
    app = FastAPI(description=description , openapi_tags=tags_metadata, dependencies=[Depends(authenticate)])
    initialize_routers(app)
    return app