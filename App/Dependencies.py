from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi import HTTPException, Depends, Request
from http import HTTPStatus
from BL import EventManager



security = HTTPBasic()

API_USERNAME = "admin"
API_PASSWORD = "admin"


def authenticate(credentials: HTTPBasicCredentials = Depends(security)):
    if API_USERNAME is None or API_PASSWORD is None:
        raise HTTPException(status_code=HTTPStatus.NON_AUTHORITATIVE_INFORMATION)
    if not (credentials.username == API_USERNAME and credentials.password == API_PASSWORD):
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED)


def bl_factory(request: Request):
    return BL_CLASS_MAP[request.url.path.split("/")[1]]()


BL_CLASS_MAP = {
    'events': EventManager,
    'users': None
}