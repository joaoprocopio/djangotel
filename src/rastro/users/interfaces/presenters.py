from typing import TypedDict

from rastro.base.presenter import Presenter
from rastro.users.application.dtos import UserOutput


class UserPublic(TypedDict):
    id: int
    email: str
    username: str
    is_active: bool
    is_verified: bool


class UserPresenter(Presenter[UserOutput, UserPublic]):
    @staticmethod
    def present(private: UserOutput) -> UserPublic:
        return UserPublic(
            id=private.id,
            email=private.email,
            username=private.username,
            is_active=private.is_active,
            is_verified=private.is_verified,
        )
