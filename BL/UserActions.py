from typing import Tuple
from http import HTTPStatus
from DL.Repositories import UsersRepo


class userActions:
    def __init__(self, user_permissions):
        self.users_repo = UsersRepo()
        self.user_permissions = 1 # TODO add precision levels for users

    def get_users(self) -> Tuple[list, HTTPStatus]:
        return NotImplemented

    def get_user_by_id(self, user_id: str) -> Tuple[dict, HTTPStatus]:
        return NotImplemented
