from typing import Optional

from rastro.conta.application.dtos import (
    CadastrarInput,
    ContaOutput,
    EntrarInput,
)
from rastro.conta.domain.errors import (
    ContaNaoEncontradaError,
    CredenciaisIncorretasError,
)
from rastro.conta.domain.repository import ContaRepository
from rastro.conta.domain.services import PasswordHashingService, SessionService
from rastro.conta.domain.value_objects import (
    Email,
    Username,
)
from rastro.conta.shared.mappers import OutputContaMapper
from rastro_base.use_case import UseCase


class ContaUseCase(UseCase):
    def __init__(
        self,
        session_service: SessionService,
    ):
        self.session_service = session_service

    def execute(self) -> Optional[ContaOutput]:
        conta = self.session_service.logged_conta()

        return OutputContaMapper.map(conta) if conta is not None else conta


class CadastrarUseCase(UseCase):
    def __init__(
        self,
        repository: ContaRepository,
        session_service: SessionService,
        password_hashing_service: PasswordHashingService,
    ):
        self.repository = repository
        self.session_service = session_service
        self.password_hashing_service = password_hashing_service

    def execute(self, input: CadastrarInput) -> ContaOutput:
        hashed_password = self.password_hashing_service.hash(input.password)

        conta = self.repository.create(
            username=input.username,
            email=input.email,
            hashed_password=hashed_password,
        )

        self.session_service.login(conta)

        return OutputContaMapper.map(conta)


class EntrarUseCase(UseCase):
    def __init__(
        self,
        repository: ContaRepository,
        session_service: SessionService,
        password_hashing_service: PasswordHashingService,
    ):
        self.repository = repository
        self.session_service = session_service
        self.password_hashing_service = password_hashing_service

    def execute(self, input: EntrarInput) -> ContaOutput:
        match input.query:
            case Email():
                conta = self.repository.get_by_email(input.query)
            case Username():
                conta = self.repository.get_by_username(input.query)

        if conta is None:
            raise ContaNaoEncontradaError()

        verification = conta.verify_password(
            input.password, self.password_hashing_service
        )

        if not verification.is_correct:
            raise CredenciaisIncorretasError()

        if verification.must_upgrade:
            self.repository.update_password(conta)

        self.session_service.login(conta)

        return OutputContaMapper.map(conta)
