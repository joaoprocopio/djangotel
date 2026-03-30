from typing import TypedDict

from rastro.base.presenter import Presenter
from rastro.users.application.dtos import UserOutput


class UserPublic(TypedDict):
    email: str
    username: str


class UserPresenter(Presenter[UserOutput, UserPublic]):
    @staticmethod
    def present(private: UserOutput) -> UserPublic:
        return UserPublic(
            email=private.email,
            username=private.username,
        )
