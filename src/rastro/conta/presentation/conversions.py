from functools import singledispatch
from typing import TYPE_CHECKING

from django.contrib.auth import get_user_model

from rastro.conta.application.dtos import ContaOutput, ContaPublic
from rastro.conta.domain.aggregates import Conta
from rastro.conta.domain.value_objects import Email, HashedPassword, Username
from rastro_shared_kernel.value_objects import Id

if TYPE_CHECKING:
    from django.contrib.auth.models import User as DjangoUser
else:
    DjangoUser = get_user_model()


def conversion_not_implemented_msg(*, source: object, target: object) -> str:
    return f"Cannot convert from {type(source).__name__} to {type(target).__name__}"


def hydrate_conta(conta: DjangoUser) -> Conta:
    return Conta(
        id=Id(conta.pk),
        username=Username(conta.username),
        email=Email(conta.email),
        password=HashedPassword(conta.password),
        first_name=conta.first_name,
        last_name=conta.last_name,
        date_joined=conta.date_joined,
        last_login=conta.last_login,
        is_superuser=conta.is_superuser,
        is_staff=conta.is_staff,
        is_active=conta.is_active,
    )


def dehydrate_conta(conta: Conta) -> DjangoUser:
    return DjangoUser(
        id=conta.id.root,
        username=conta.username.root,
        email=conta.email.root,
        password=conta.password.root,
        is_active=conta.is_active,
    )


@singledispatch
def present_conta(conta: object) -> ContaPublic:
    raise NotImplementedError(
        conversion_not_implemented_msg(source=conta, target=ContaPublic)
    )


@present_conta.register
def _(conta: Conta) -> ContaPublic:
    return ContaPublic(
        email=conta.email.root,
        username=conta.username.root,
    )


@present_conta.register
def _(conta: ContaOutput) -> ContaPublic:
    return ContaPublic(
        email=conta.email,
        username=conta.username,
    )


@singledispatch
def output_conta(conta: object) -> ContaOutput:
    raise NotImplementedError(
        conversion_not_implemented_msg(source=conta, target=ContaOutput)
    )


@output_conta.register
def _(conta: Conta) -> ContaOutput:
    return ContaOutput(
        id=conta.id,
        username=conta.username,
        email=conta.email,
        password=conta.password,
        first_name=conta.first_name,
        last_name=conta.last_name,
        date_joined=conta.date_joined,
        last_login=conta.last_login,
        is_superuser=conta.is_superuser,
        is_staff=conta.is_staff,
        is_active=conta.is_active,
    )
