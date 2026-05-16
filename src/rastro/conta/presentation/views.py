from http import HTTPStatus
from typing import Callable

from django.http import HttpRequest, HttpResponse, JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import ensure_csrf_cookie

from rastro.conta.application.dtos import CadastrarInput, EntrarInput
from rastro.conta.application.use_cases import (
    CadastrarUseCase,
    ContaUseCase,
    EntrarUseCase,
    SairUseCase,
)
from rastro.conta.infrastructure.composition import (
    make_django_cadastrar_use_case,
    make_django_conta_use_case,
    make_django_entrar_use_case,
    make_django_sair_use_case,
)
from rastro.conta.shared.mappers import PresentContaMapper


@method_decorator(ensure_csrf_cookie, name="dispatch")
class CsrfTokenView(View):
    def get(self, _: HttpRequest) -> HttpResponse:
        return HttpResponse(status=HTTPStatus.OK)


class ContaView(View):
    make_conta_use_case: Callable[[HttpRequest], ContaUseCase] = (
        make_django_conta_use_case
    )

    def get(self, request: HttpRequest) -> HttpResponse:
        conta_use_case = self.make_conta_use_case(request)
        conta = conta_use_case.execute()

        if conta is None:
            return HttpResponse(status=HTTPStatus.UNAUTHORIZED)

        return JsonResponse(
            PresentContaMapper.map(conta).model_dump(),
            status=HTTPStatus.OK,
        )


class EntrarView(View):
    make_entrar_use_case: Callable[[HttpRequest], EntrarUseCase] = (
        make_django_entrar_use_case
    )

    def post(self, request: HttpRequest) -> HttpResponse:
        entrar_use_case = self.make_entrar_use_case(request)
        entrar_input = EntrarInput.model_validate_json(request.body)
        conta_output = entrar_use_case.execute(entrar_input)

        return JsonResponse(
            PresentContaMapper.map(conta_output).model_dump(),
            status=HTTPStatus.OK,
        )


class CadastrarView(View):
    make_cadastrar_use_case: Callable[[HttpRequest], CadastrarUseCase] = (
        make_django_cadastrar_use_case
    )

    def post(self, request: HttpRequest) -> HttpResponse:
        cadastrar_use_case = self.make_cadastrar_use_case(request)
        input = CadastrarInput.model_validate_json(request.body)
        output = cadastrar_use_case.execute(input)

        return JsonResponse(
            PresentContaMapper.map(output).model_dump(),
            status=HTTPStatus.CREATED,
        )


class SairView(View):
    make_sair_use_case: Callable[[HttpRequest], SairUseCase] = make_django_sair_use_case

    def post(self, request: HttpRequest) -> HttpResponse:
        sair_use_case = self.make_sair_use_case(request)
        sair_use_case.execute()

        return HttpResponse(status=HTTPStatus.OK)
