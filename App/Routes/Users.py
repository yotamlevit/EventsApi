from fastapi import APIRouter, Depends, Body


users_api = APIRouter(
    prefix="/users",
    tags=["Users API"]
)


@users_api.get()
def get_users():
    pass


@users_api.get("/{user_name}")
def get_user(user_name: str):
    pass

@users_api.delete("/{user_name}")
def delete_user(user_name: str):
    pass

@users_api.put("/{user_name}")
def update_user(user_name: str, user_data : dict = Body()):
    pass


@users_api.post("/{user_name}")
def create_user(user_name: str, user_data : dict = Body()):
    pass