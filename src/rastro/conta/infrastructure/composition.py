from django.http import HttpRequest

from rastro.conta.application.use_cases import (
    CadastrarUseCase,
    ContaUseCase,
    EntrarUseCase,
)
from rastro.conta.infrastructure.repositories import DjangoContaRepository
from rastro.conta.infrastructure.services import (
    DjangoPasswordHashingService,
    DjangoSessionService,
)


def make_django_conta_use_case(request: HttpRequest) -> ContaUseCase:
    session_service = DjangoSessionService(request)
    conta_use_case = ContaUseCase(session_service)

    return conta_use_case


def make_django_entrar_use_case(request: HttpRequest) -> EntrarUseCase:
    repository = DjangoContaRepository()
    password_hashing_service = DjangoPasswordHashingService()
    session_service = DjangoSessionService(request)
    entrar_use_case = EntrarUseCase(
        repository, session_service, password_hashing_service
    )

    return entrar_use_case


def make_django_cadastrar_use_case(request: HttpRequest) -> CadastrarUseCase:
    repository = DjangoContaRepository()
    password_hashing_service = DjangoPasswordHashingService()
    session_service = DjangoSessionService(request)
    cadastrar_use_case = CadastrarUseCase(
        repository, session_service, password_hashing_service
    )

    return cadastrar_use_case
