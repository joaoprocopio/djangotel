from dataclasses import dataclass


@dataclass(frozen=True)
class SignUpInput:
    username: str
    email: str
    password: str


@dataclass(frozen=True)
class SignInInput:
    query: str
    password: str


@dataclass(frozen=True)
class UserOutput:
    id: int
    email: str
    username: str
    is_active: bool
    is_verified: bool


@dataclass(frozen=True)
class RequestPasswordResetInput:
    email: str


@dataclass(frozen=True)
class ResetPasswordInput:
    user_id: int
    token: str
    new_password: str


@dataclass(frozen=True)
class RequestEmailVerificationInput:
    user_id: int


@dataclass(frozen=True)
class VerifyEmailInput:
    user_id: int
    token: str


@dataclass(frozen=True)
class GetUserInput:
    user_id: int
