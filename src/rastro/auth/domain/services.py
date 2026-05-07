from abc import abstractmethod
from typing import NamedTuple, Optional

from rastro.auth.domain.entities import User
from rastro.auth.domain.value_objects import HashedPassword, RawPassword
from rastro_base.service import Service


class PasswordVerification(NamedTuple):
    is_correct: bool
    must_upgrade: bool


class PasswordHashingService(Service):
    @abstractmethod
    def hash(self, raw_password: RawPassword) -> HashedPassword: ...

    @abstractmethod
    def verify(
        self, raw_password: RawPassword, hashed_password: HashedPassword
    ) -> PasswordVerification: ...


class SessionService(Service):
    @abstractmethod
    def login(self, user: User) -> None: ...

    @abstractmethod
    def logout(self) -> None: ...

    @abstractmethod
    def logged_user(self) -> Optional[User]: ...
