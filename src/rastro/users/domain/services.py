from abc import abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from django.http import HttpRequest

from rastro.base.domain_service import DomainService
from rastro.base.entity import Id
from rastro.users.domain.user import User
from rastro.users.domain.value_objects import HashedPassword, RawPassword


class PasswordHashingService(DomainService):
    @abstractmethod
    def hash(self, password: RawPassword) -> HashedPassword: ...

    @abstractmethod
    def verify(self, password: RawPassword, hashed: HashedPassword) -> bool: ...


class SessionService(DomainService):
    @abstractmethod
    def login(self, request: "HttpRequest", user_id: Id) -> None: ...

    @abstractmethod
    def logout(self, request: "HttpRequest") -> None: ...

    @abstractmethod
    def get_current_user_id(self, request: "HttpRequest") -> Id | None: ...


class EmailService(DomainService):
    @abstractmethod
    def send_verification_email(self, user: User, token: str) -> None: ...

    @abstractmethod
    def send_password_reset_email(self, user: User, token: str) -> None: ...


class TokenService(DomainService):
    @abstractmethod
    def generate_verification_token(self, user: User) -> str: ...

    @abstractmethod
    def generate_password_reset_token(self, user: User) -> str: ...

    @abstractmethod
    def verify_token(self, token: str, token_type: str) -> Id | None: ...
