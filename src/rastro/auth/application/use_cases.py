from rastro.auth.application.dtos import (
    SignInInput,
    SignUpInput,
    UserOutput,
)
from rastro.auth.domain.errors import (
    AuthenticationError,
    UserNotFoundError,
)
from rastro.auth.domain.repository import UserRepository
from rastro.auth.domain.services import PasswordHashingService
from rastro.auth.domain.value_objects import (
    Email,
    Username,
)
from rastro.auth.infrastructure.mappers import DomainToOutputUserMapper
from rastro_base.use_case import UseCase


class SignUpUseCase(UseCase[SignUpInput, UserOutput]):
    def __init__(
        self,
        repository: UserRepository,
        password_hashing_service: PasswordHashingService,
    ):
        self.repository = repository
        self.password_hashing_service = password_hashing_service

    def execute(self, input: SignUpInput) -> UserOutput:
        hashed_password = self.password_hashing_service.hash(input.password)

        user = self.repository.create(
            username=input.username,
            email=input.email,
            hashed_password=hashed_password,
        )

        return DomainToOutputUserMapper.map(user)


class SignInUseCase(UseCase[SignInInput, UserOutput]):
    def __init__(
        self,
        repository: UserRepository,
        password_hashing_service: PasswordHashingService,
    ):
        self.repository = repository
        self.password_hashing_service = password_hashing_service

    def execute(self, input: SignInInput) -> UserOutput:
        match input.query:
            case Email():
                user = self.repository.get_by_email(input.query)
            case Username():
                user = self.repository.get_by_username(input.query)

        if user is None:
            raise UserNotFoundError()

        if not user.check_password(input.password, self.password_hashing_service):
            raise AuthenticationError()

        return DomainToOutputUserMapper.map(user)
