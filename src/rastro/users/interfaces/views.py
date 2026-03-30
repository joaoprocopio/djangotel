from django.http import HttpRequest

from rastro.base.entity import Id
from rastro.users.application.dtos import (
    GetUserInput,
    ResetPasswordInput,
    SignInInput,
    SignUpInput,
    UserOutput,
    VerifyEmailInput,
)
from rastro.users.application.use_cases import (
    GetUserUseCase,
    RequestPasswordResetUseCase,
    ResetPasswordUseCase,
    SignInUseCase,
    SignUpUseCase,
    VerifyEmailUseCase,
)
from rastro.users.infrastructure.repository import DjangoUserRepository
from rastro.users.infrastructure.services import (
    DjangoPasswordHashingService,
    DjangoSessionService,
    DjangoTokenService,
)
from rastro.users.interfaces.presenters import UserPresenter, UserPublic

repository = DjangoUserRepository()
password_hashing_service = DjangoPasswordHashingService()
session_service = DjangoSessionService()
token_service = DjangoTokenService()

sign_up_use_case = SignUpUseCase(repository, password_hashing_service)
sign_in_use_case = SignInUseCase(repository, password_hashing_service)
get_user_use_case = GetUserUseCase(repository)
request_password_reset_use_case = RequestPasswordResetUseCase(repository, token_service)
reset_password_use_case = ResetPasswordUseCase(
    repository, token_service, password_hashing_service
)
verify_email_use_case = VerifyEmailUseCase(repository, token_service)


def sign_up(request: HttpRequest) -> UserPublic:
    import json

    data = json.loads(request.body)
    input_dto = SignUpInput(
        username=data["username"],
        email=data["email"],
        password=data["password"],
    )
    output: UserOutput = sign_up_use_case.execute(input_dto)
    return UserPresenter.present(output)


def sign_in(request: HttpRequest) -> UserPublic:
    import json

    data = json.loads(request.body)
    input_dto = SignInInput(
        query=data["query"],
        password=data["password"],
    )
    output: UserOutput = sign_in_use_case.execute(input_dto)
    session_service.login(request, Id(output.id))
    return UserPresenter.present(output)


def sign_out(request: HttpRequest) -> None:
    session_service.logout(request)


def current_user(request: HttpRequest) -> UserPublic | None:
    user_id = session_service.get_current_user_id(request)
    if user_id is None:
        return None
    input_dto = GetUserInput(user_id=user_id.value)
    output: UserOutput = get_user_use_case.execute(input_dto)
    return UserPresenter.present(output)


def request_password_reset(request: HttpRequest) -> str:
    import json

    data = json.loads(request.body)
    email = data["email"]
    return request_password_reset_use_case.execute(email)


def reset_password(request: HttpRequest) -> UserPublic:
    import json

    data = json.loads(request.body)
    input_dto = ResetPasswordInput(
        user_id=data["user_id"],
        token=data["token"],
        new_password=data["new_password"],
    )
    output: UserOutput = reset_password_use_case.execute(input_dto)
    return UserPresenter.present(output)


def verify_email(request: HttpRequest) -> UserPublic:
    import json

    data = json.loads(request.body)
    input_dto = VerifyEmailInput(
        user_id=data["user_id"],
        token=data["token"],
    )
    output: UserOutput = verify_email_use_case.execute(input_dto)
    return UserPresenter.present(output)
