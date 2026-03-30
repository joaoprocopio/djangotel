from dataclasses import dataclass


@dataclass(frozen=True)
class SignUpRequest:
    username: str
    email: str
    password: str


@dataclass(frozen=True)
class SignInRequest:
    query: str
    password: str


@dataclass(frozen=True)
class ResetPasswordRequest:
    user_id: int
    token: str
    new_password: str


@dataclass(frozen=True)
class VerifyEmailRequest:
    user_id: int
    token: str


@dataclass(frozen=True)
class RequestPasswordResetRequest:
    email: str


@dataclass(frozen=True)
class UserResponse:
    id: int
    username: str
    email: str
    is_active: bool
    is_verified: bool
