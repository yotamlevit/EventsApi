from fastapi import APIRouter, Depends, Body
from fastapi.responses import JSONResponse
from http import HTTPStatus

users_api = APIRouter(
    prefix="/users",
    tags=["Users API"]
)


@users_api.get("")
def get_users():
    return JSONResponse(status_code=HTTPStatus.NOT_IMPLEMENTED, content={"message": "Not implemented"})


@users_api.get("/{user_name}")
def get_user(user_name: str):
    return JSONResponse(status_code=HTTPStatus.NOT_IMPLEMENTED, content={"message": "Not implemented"})

@users_api.delete("/{user_name}")
def delete_user(user_name: str):
    return JSONResponse(status_code=HTTPStatus.NOT_IMPLEMENTED, content={"message": "Not implemented"})

@users_api.put("/{user_name}")
def update_user(user_name: str, user_data : dict = Body()):
    return JSONResponse(status_code=HTTPStatus.NOT_IMPLEMENTED, content={"message": "Not implemented"})


@users_api.post("/{user_name}")
def create_user(user_name: str, user_data : dict = Body()):
    return JSONResponse(status_code=HTTPStatus.NOT_IMPLEMENTED, content={"message": "Not implemented"})


@users_api.get("/{user_name}/permissions")
def get_user_permissions(user_name: str):
    return JSONResponse(status_code=HTTPStatus.NOT_IMPLEMENTED, content={"message": "Not implemented"})


@users_api.put("/{user_name}/permissions")
def get_user_permissions(user_name: str, permissions_level : dict = Body()):
    return JSONResponse(status_code=HTTPStatus.NOT_IMPLEMENTED, content={"message": "Not implemented"})