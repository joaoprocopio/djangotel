from abc import abstractmethod

from rastro.base.service import Service
from rastro.users.domain.entities import User
from rastro.users.domain.value_objects import HashedPassword, RawPassword


class PasswordHashingService(Service):
    @abstractmethod
    def hash(self, raw_password: RawPassword) -> HashedPassword: ...

    @abstractmethod
    def verify(
        self, raw_password: RawPassword, hashed_password: HashedPassword
    ) -> bool: ...


class SessionService(Service):
    @abstractmethod
    def login(self, user: User) -> None: ...

    @abstractmethod
    def logout(self) -> None: ...

    @abstractmethod
    def logged_user(self) -> User | None: ...
