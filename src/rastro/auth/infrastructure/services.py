from typing import Optional

from django.contrib import auth
from django.contrib.auth.hashers import make_password, verify_password
from django.http import HttpRequest

from rastro.auth.domain.aggregates import User
from rastro.auth.domain.services import (
    PasswordHashingService,
    PasswordVerification,
    SessionService,
)
from rastro.auth.domain.value_objects import HashedPassword, RawPassword
from rastro.auth.presentation.mappers import (
    DehydrateUser,
    DomainToDjangoUserMapper,
)


class DjangoSessionService(SessionService):
    def __init__(self, request: HttpRequest) -> None:
        self.request = request

    def login(self, user: User) -> None:
        auth.login(self.request, DomainToDjangoUserMapper.map(user))

    def logout(self) -> None:
        auth.logout(self.request)

    def logged_user(self) -> Optional[User]:
        user = auth.get_user(self.request)

        if user.pk is None:
            return None

        return DehydrateUser.map(user)


class DjangoPasswordHashingService(PasswordHashingService):
    def hash(self, raw_password: RawPassword) -> HashedPassword:
        return HashedPassword(make_password(raw_password.root))

    def verify(
        self, raw_password: RawPassword, hashed_password: HashedPassword
    ) -> PasswordVerification:
        is_correct, must_upgrade = verify_password(
            raw_password.root, hashed_password.root
        )

        return PasswordVerification(is_correct=is_correct, must_upgrade=must_upgrade)
