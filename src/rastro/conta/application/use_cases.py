from rastro.conta.application.dtos import (
    SignInInput,
    SignUpInput,
    UserOutput,
)
from rastro.conta.domain.errors import (
    AuthenticationError,
    UserNotFoundError,
)
from rastro.conta.domain.repository import UserRepository
from rastro.conta.domain.services import PasswordHashingService, SessionService
from rastro.conta.domain.value_objects import (
    Email,
    Username,
)
from rastro.conta.presentation.mappers import (
    DomainToOutputUserMapper,
)
from rastro_base.use_case import UseCase


class SignUpUseCase(UseCase[SignUpInput, UserOutput]):
    def __init__(
        self,
        repository: UserRepository,
        session_service: SessionService,
        password_hashing_service: PasswordHashingService,
    ):
        self.repository = repository
        self.session_service = session_service
        self.password_hashing_service = password_hashing_service

    def execute(self, input: SignUpInput) -> UserOutput:
        hashed_password = self.password_hashing_service.hash(input.password)

        user = self.repository.create(
            username=input.username,
            email=input.email,
            hashed_password=hashed_password,
        )

        self.session_service.login(user)

        return DomainToOutputUserMapper.map(user)


class SignInUseCase(UseCase[SignInInput, UserOutput]):
    def __init__(
        self,
        repository: UserRepository,
        session_service: SessionService,
        password_hashing_service: PasswordHashingService,
    ):
        self.repository = repository
        self.session_service = session_service
        self.password_hashing_service = password_hashing_service

    def execute(self, input: SignInInput) -> UserOutput:
        match input.query:
            case Email():
                user = self.repository.get_by_email(input.query)
            case Username():
                user = self.repository.get_by_username(input.query)

        if user is None:
            raise UserNotFoundError()

        verification = user.verify_password(
            input.password, self.password_hashing_service
        )

        if not verification.is_correct:
            raise AuthenticationError()

        if verification.must_upgrade:
            self.repository.update_password(user)

        self.session_service.login(user)

        return DomainToOutputUserMapper.map(user)
