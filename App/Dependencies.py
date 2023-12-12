from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi import HTTPException, Depends
from http import HTTPStatus


security = HTTPBasic()

API_USERNAME = "admin"
API_PASSWORD = "admin"


def authenticate(credentials: HTTPBasicCredentials = Depends(security)):
    if API_USERNAME is None or API_PASSWORD is None:
        raise HTTPException(status_code=HTTPStatus.NON_AUTHORITATIVE_INFORMATION)
    if not (credentials.username == API_USERNAME and credentials.password == API_PASSWORD):
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED)