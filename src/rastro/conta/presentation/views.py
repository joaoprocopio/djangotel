from http import HTTPStatus

from django.http import HttpRequest, HttpResponse, JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import ensure_csrf_cookie

from rastro.conta.application.dtos import CadastrarInput, EntrarInput
from rastro.conta.infrastructure.services import (
    DjangoSessionService,
)
from rastro.conta.presentation.conversions import present_conta
from rastro.conta.presentation.dependencies import (
    DjangoCadastrarUseCaseFactory,
    DjangoEntrarUseCaseFactory,
)


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
    entrar_use_case_factory: DjangoEntrarUseCaseFactory

    def post(self, request: HttpRequest) -> HttpResponse:
        entrar_use_case = self.entrar_use_case_factory(request)
        entrar_input = EntrarInput.model_validate_json(request.body)
        conta_output = entrar_use_case.execute(entrar_input)

        return JsonResponse(
            present_conta(conta_output).model_dump(),
            status=HTTPStatus.OK,
        )


class CadastrarView(View):
    cadastrar_use_case_factory: DjangoCadastrarUseCaseFactory

    def post(self, request: HttpRequest) -> HttpResponse:
        cadastrar_use_case = self.cadastrar_use_case_factory(request)
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
