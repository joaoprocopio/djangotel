from http import HTTPStatus

from django.http import HttpRequest, HttpResponse, JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import ensure_csrf_cookie

from rastro.conta.application.dtos import CadastrarInput, EntrarInput
from rastro.conta.application.use_cases import CadastrarUseCase, EntrarUseCase
from rastro.conta.infrastructure.repositories import DjangoUserRepository
from rastro.conta.infrastructure.services import (
    DjangoPasswordHashingService,
    DjangoSessionService,
)
from rastro.conta.presentation.conversions import present_conta


@method_decorator(ensure_csrf_cookie, name="get")
class CsrfTokenView(View):
    def get(self, _: HttpRequest) -> HttpResponse:
        return HttpResponse(status=HTTPStatus.OK)


class ContaView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        session_service = DjangoSessionService(request)
        user = session_service.logged_user()

        if user is None:
            return HttpResponse(status=HTTPStatus.UNAUTHORIZED)

        return JsonResponse(
            present_conta(user).model_dump(),
            status=HTTPStatus.OK,
        )


class EntrarView(View):
    def post(self, request: HttpRequest) -> HttpResponse:
        repository = DjangoUserRepository()
        password_hashing_service = DjangoPasswordHashingService()
        session_service = DjangoSessionService(request)
        entrar_use_case = EntrarUseCase(
            repository, session_service, password_hashing_service
        )

        input = EntrarInput.model_validate_json(request.body)
        output = entrar_use_case.execute(input)

        return JsonResponse(
            present_conta(output).model_dump(),
            status=HTTPStatus.OK,
        )


class CadastrarView(View):
    def post(self, request: HttpRequest) -> HttpResponse:
        repository = DjangoUserRepository()
        password_hashing_service = DjangoPasswordHashingService()
        session_service = DjangoSessionService(request)
        cadastrar_use_case = CadastrarUseCase(
            repository, session_service, password_hashing_service
        )

        input = CadastrarInput.model_validate_json(request.body)
        output = cadastrar_use_case.execute(input)

        return JsonResponse(
            present_conta(output).model_dump(),
            status=HTTPStatus.CREATED,
        )


class SairView(View):
    def post(self, request: HttpRequest) -> HttpResponse:
        session_service = DjangoSessionService(request)
        user = session_service.logged_user()

        if user is None:
            return HttpResponse(status=HTTPStatus.UNAUTHORIZED)

        session_service.logout()

        return HttpResponse(status=HTTPStatus.NO_CONTENT)
