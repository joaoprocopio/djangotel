from dataclasses import dataclass

from rastro.base.domain_event import DomainEvent


@dataclass(frozen=True, kw_only=True)
class UserRegistered(DomainEvent):
    user_id: int
    email: str
    username: str


@dataclass(frozen=True, kw_only=True)
class UserLoggedIn(DomainEvent):
    user_id: int


@dataclass(frozen=True, kw_only=True)
class UserLoggedOut(DomainEvent):
    user_id: int


@dataclass(frozen=True, kw_only=True)
class UserPasswordResetRequested(DomainEvent):
    user_id: int
    email: str
    token: str


@dataclass(frozen=True, kw_only=True)
class UserPasswordResetCompleted(DomainEvent):
    user_id: int


@dataclass(frozen=True, kw_only=True)
class UserEmailVerificationRequested(DomainEvent):
    user_id: int
    email: str
    token: str


@dataclass(frozen=True, kw_only=True)
class UserEmailVerified(DomainEvent):
    user_id: int
