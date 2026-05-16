from typing import TYPE_CHECKING

from django.contrib.auth import get_user_model

from rastro.conta.application.dtos import ContaOutput, ContaPublic
from rastro.conta.domain.aggregates import Conta
from rastro.conta.domain.value_objects import Email, HashedPassword, Username
from rastro_base.mapper import Mapper
from rastro_shared_kernel.value_objects import Id

if TYPE_CHECKING:
    from django.contrib.auth.models import User
else:
    User = get_user_model()


class HydrateContaMapper(Mapper[User, Conta]):
    @staticmethod
    def map(conta: User) -> Conta:
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


class DehydrateContaMapper(Mapper[Conta, User]):
    @staticmethod
    def map(conta: Conta) -> User:
        return User(
            id=conta.id.root,
            username=conta.username.root,
            email=conta.email.root,
            password=conta.password.root,
            first_name=conta.first_name,
            last_name=conta.last_name,
            date_joined=conta.date_joined,
            last_login=conta.last_login,
            is_superuser=conta.is_superuser,
            is_staff=conta.is_staff,
            is_active=conta.is_active,
        )


class PresentContaMapper(Mapper[Conta | ContaOutput, ContaPublic]):
    @staticmethod
    def map(source: Conta | ContaOutput) -> ContaPublic:
        match source:
            case Conta():
                return ContaPublic(
                    email=source.email,
                    username=source.username,
                )
            case ContaOutput():
                return ContaPublic(
                    email=source.email,
                    username=source.username,
                )


class OutputContaMapper(Mapper[Conta, ContaOutput]):
    @staticmethod
    def map(source: Conta) -> ContaOutput:
        return ContaOutput(
            id=source.id,
            username=source.username,
            email=source.email,
            password=source.password,
            first_name=source.first_name,
            last_name=source.last_name,
            date_joined=source.date_joined,
            last_login=source.last_login,
            is_superuser=source.is_superuser,
            is_staff=source.is_staff,
            is_active=source.is_active,
        )
