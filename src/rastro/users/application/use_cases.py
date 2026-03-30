from typing import TYPE_CHECKING

from rastro.base.entity import Id
from rastro.base.use_case import UseCase
from rastro.users.application.dtos import (
    GetUserInput,
    ResetPasswordInput,
    SignInInput,
    SignUpInput,
    UserOutput,
    VerifyEmailInput,
)
from rastro.users.domain.errors import (
    AuthenticationError,
    EmailAlreadyExistsError,
    InvalidTokenError,
    UsernameAlreadyExistsError,
    UserNotFoundError,
)
from rastro.users.domain.events import (
    UserEmailVerified,
    UserLoggedIn,
    UserPasswordResetCompleted,
    UserPasswordResetRequested,
    UserRegistered,
)
from rastro.users.domain.repository import UserRepository
from rastro.users.domain.services import (
    PasswordHashingService,
    TokenService,
)
from rastro.users.domain.value_objects import Email, RawPassword, Username


class SignUpUseCase(UseCase[SignUpInput, UserOutput]):
    def __init__(
        self,
        repository: UserRepository,
        password_hashing_service: PasswordHashingService,
    ):
        self._repository = repository
        self._password_hashing_service = password_hashing_service

    def execute(self, input: SignUpInput) -> UserOutput:
        email = Email(input.email)
        username = Username(input.username)
        raw_password = RawPassword(input.password)

        if self._repository.exists_by_email(email):
            raise EmailAlreadyExistsError(f"Email {input.email} already exists")

        if self._repository.exists_by_username(username):
            raise UsernameAlreadyExistsError(
                f"Username {input.username} already exists"
            )

        hashed_password = self._password_hashing_service.hash(raw_password)

        user = self._repository.create(username, email, hashed_password)

        user.add_domain_event(
            UserRegistered(
                user_id=user.id.value,
                email=input.email,
                username=input.username,
            )
        )

        return UserOutput(
            id=user.id.value,
            email=user.email.value,
            username=user.username.value,
            is_active=user.is_active,
            is_verified=user.is_verified,
        )


class SignInUseCase(UseCase[SignInInput, UserOutput]):
    def __init__(
        self,
        repository: UserRepository,
        password_hashing_service: PasswordHashingService,
    ):
        self._repository = repository
        self._password_hashing_service = password_hashing_service

    def execute(self, input: SignInInput) -> UserOutput:
        if "@" in input.query:
            user = self._repository.get_by_email(Email(input.query))
        else:
            user = self._repository.get_by_username(Username(input.query))

        if user is None:
            raise AuthenticationError("Invalid credentials")

        raw_password = RawPassword(input.password)

        if not self._password_hashing_service.verify(
            raw_password, user.hashed_password
        ):
            raise AuthenticationError("Invalid credentials")

        user.add_domain_event(UserLoggedIn(user_id=user.id.value))

        return UserOutput(
            id=user.id.value,
            email=user.email.value,
            username=user.username.value,
            is_active=user.is_active,
            is_verified=user.is_verified,
        )


class RequestPasswordResetUseCase(UseCase[str, str]):
    def __init__(
        self,
        repository: UserRepository,
        token_service: TokenService,
    ):
        self._repository = repository
        self._token_service = token_service

    def execute(self, input: str) -> str:
        email = input
        user = self._repository.get_by_email(Email(email))
        if user is None:
            raise UserNotFoundError(f"User with email {email} not found")

        token = self._token_service.generate_password_reset_token(user)

        user.add_domain_event(
            UserPasswordResetRequested(
                user_id=user.id.value,
                email=user.email.value,
                token=token,
            )
        )

        return token


class ResetPasswordUseCase(UseCase[ResetPasswordInput, UserOutput]):
    def __init__(
        self,
        repository: UserRepository,
        token_service: TokenService,
        password_hashing_service: PasswordHashingService,
    ):
        self._repository = repository
        self._token_service = token_service
        self._password_hashing_service = password_hashing_service

    def execute(self, input: ResetPasswordInput) -> UserOutput:
        user_id = Id(input.user_id)
        user = self._repository.get_by_id(user_id)
        if user is None:
            raise UserNotFoundError(f"User with id {input.user_id} not found")

        if self._token_service.verify_token(input.token, "password_reset") is None:
            raise InvalidTokenError("Invalid or expired token")

        raw_password = RawPassword(input.new_password)
        hashed_password = self._password_hashing_service.hash(raw_password)

        user.update_password(hashed_password)
        user.add_domain_event(UserPasswordResetCompleted(user_id=user.id.value))

        saved_user = self._repository.update(user)

        return UserOutput(
            id=saved_user.id.value,
            email=saved_user.email.value,
            username=saved_user.username.value,
            is_active=saved_user.is_active,
            is_verified=saved_user.is_verified,
        )


class VerifyEmailUseCase(UseCase[VerifyEmailInput, UserOutput]):
    def __init__(
        self,
        repository: UserRepository,
        token_service: TokenService,
    ):
        self._repository = repository
        self._token_service = token_service

    def execute(self, input: VerifyEmailInput) -> UserOutput:
        user_id = Id(input.user_id)
        user = self._repository.get_by_id(user_id)
        if user is None:
            raise UserNotFoundError(f"User with id {input.user_id} not found")

        if self._token_service.verify_token(input.token, "email_verification") is None:
            raise InvalidTokenError("Invalid or expired token")

        user.verify_email()
        user.add_domain_event(UserEmailVerified(user_id=user.id.value))

        saved_user = self._repository.update(user)

        return UserOutput(
            id=saved_user.id.value,
            email=saved_user.email.value,
            username=saved_user.username.value,
            is_active=saved_user.is_active,
            is_verified=saved_user.is_verified,
        )


class GetUserUseCase(UseCase[GetUserInput, UserOutput]):
    def __init__(self, repository: UserRepository):
        self._repository = repository

    def execute(self, input: GetUserInput) -> UserOutput:
        user_id = Id(input.user_id)
        user = self._repository.get_by_id(user_id)
        if user is None:
            raise UserNotFoundError(f"User with id {input.user_id} not found")

        return UserOutput(
            id=user.id.value,
            email=user.email.value,
            username=user.username.value,
            is_active=user.is_active,
            is_verified=user.is_verified,
        )
