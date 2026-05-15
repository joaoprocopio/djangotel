from typing import Protocol

from django.http import HttpRequest

from rastro.conta.application.use_cases import CadastrarUseCase, EntrarUseCase
from rastro.conta.infrastructure.repositories import DjangoContaRepository
from rastro.conta.infrastructure.services import (
    DjangoPasswordHashingService,
    DjangoSessionService,
)


class DjangoEntrarUseCaseFactory(Protocol):
    def __call__(self, request: HttpRequest) -> EntrarUseCase:
        repository = DjangoContaRepository()
        password_hashing_service = DjangoPasswordHashingService()
        session_service = DjangoSessionService(request)
        entrar_use_case = EntrarUseCase(
            repository, session_service, password_hashing_service
        )

        return entrar_use_case


class DjangoCadastrarUseCaseFactory(Protocol):
    def __call__(self, request: HttpRequest) -> CadastrarUseCase:
        repository = DjangoContaRepository()
        password_hashing_service = DjangoPasswordHashingService()
        session_service = DjangoSessionService(request)
        cadastrar_use_case = CadastrarUseCase(
            repository, session_service, password_hashing_service
        )

        return cadastrar_use_case
