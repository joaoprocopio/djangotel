from http import HTTPStatus
from typing import Callable

from django.http import HttpRequest, HttpResponse, JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import ensure_csrf_cookie

from rastro.conta.application.dtos import CadastrarInput, EntrarInput
from rastro.conta.application.use_cases import CadastrarUseCase, EntrarUseCase
from rastro.conta.infrastructure.dependencies import (
    django_cadastrar_use_case_factory,
    django_entrar_use_case_dependency,
)
from rastro.conta.infrastructure.services import (
    DjangoSessionService,
)
from rastro.conta.shared.mappers import PresentContaMapper


@method_decorator(ensure_csrf_cookie, name="dispatch")
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
            PresentContaMapper.map(user).model_dump(),
            status=HTTPStatus.OK,
        )


class EntrarView(View):
    entrar_use_case_factory: Callable[[HttpRequest], EntrarUseCase] = (
        django_entrar_use_case_dependency
    )

    def post(self, request: HttpRequest) -> HttpResponse:
        entrar_use_case = self.entrar_use_case_factory(request)
        entrar_input = EntrarInput.model_validate_json(request.body)
        conta_output = entrar_use_case.execute(entrar_input)

        return JsonResponse(
            PresentContaMapper.map(conta_output).model_dump(),
            status=HTTPStatus.OK,
        )


class CadastrarView(View):
    cadastrar_use_case_factory: Callable[[HttpRequest], CadastrarUseCase] = (
        django_cadastrar_use_case_factory
    )

    def post(self, request: HttpRequest) -> HttpResponse:
        cadastrar_use_case = self.cadastrar_use_case_factory(request)
        input = CadastrarInput.model_validate_json(request.body)
        output = cadastrar_use_case.execute(input)

        return JsonResponse(
            PresentContaMapper.map(output).model_dump(),
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
