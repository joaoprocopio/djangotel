from http import HTTPStatus

from django.http import HttpRequest, HttpResponse, JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import ensure_csrf_cookie

from rastro.conta.application.dtos import SignInInput, SignUpInput
from rastro.conta.application.use_cases import SignInUseCase, SignUpUseCase
from rastro.conta.infrastructure.repositories import DjangoUserRepository
from rastro.conta.infrastructure.services import (
    DjangoPasswordHashingService,
    DjangoSessionService,
)
from rastro.conta.presentation.mappers import (
    DomainToPublicUserMapper,
    OutputToPublicUserMapper,
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
            DomainToPublicUserMapper.map(user).model_dump(),
            status=HTTPStatus.OK,
        )


class SignInView(View):
    def post(self, request: HttpRequest) -> HttpResponse:
        repository = DjangoUserRepository()
        password_hashing_service = DjangoPasswordHashingService()
        session_service = DjangoSessionService(request)
        sign_in_use_case = SignInUseCase(
            repository, session_service, password_hashing_service
        )

        input = SignInInput.model_validate_json(request.body)
        output = sign_in_use_case.execute(input)

        return JsonResponse(
            OutputToPublicUserMapper.map(output).model_dump(),
            status=HTTPStatus.OK,
        )


class SignUpView(View):
    def post(self, request: HttpRequest) -> HttpResponse:
        repository = DjangoUserRepository()
        password_hashing_service = DjangoPasswordHashingService()
        session_service = DjangoSessionService(request)
        sign_up_use_case = SignUpUseCase(
            repository, session_service, password_hashing_service
        )

        input = SignUpInput.model_validate_json(request.body)
        output = sign_up_use_case.execute(input)

        return JsonResponse(
            OutputToPublicUserMapper.map(output).model_dump(),
            status=HTTPStatus.CREATED,
        )


class SignOutView(View):
    def post(self, request: HttpRequest) -> HttpResponse:
        session_service = DjangoSessionService(request)
        user = session_service.logged_user()

        if user is None:
            return HttpResponse(status=HTTPStatus.UNAUTHORIZED)

        session_service.logout()

        return HttpResponse(status=HTTPStatus.NO_CONTENT)
