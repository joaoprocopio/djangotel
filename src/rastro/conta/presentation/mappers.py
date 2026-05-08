from typing import TYPE_CHECKING

from django.contrib.auth import get_user_model

from rastro.conta.application.dtos import ContaOutput, ContaPublic
from rastro.conta.domain.aggregates import Conta
from rastro.conta.domain.value_objects import Email, HashedPassword, Username
from rastro_base.mapper import Mapper
from rastro_shared_kernel.value_objects import Id

if TYPE_CHECKING:
    from django.contrib.auth.models import User as DjangoUser
else:
    DjangoUser = get_user_model()


class HydrateConta(Mapper[DjangoUser, Conta]):
    @staticmethod
    def map(input: DjangoUser) -> Conta:
        return Conta(
            id=Id(input.pk),
            username=Username(input.username),
            email=Email(input.email),
            password=HashedPassword(input.password),
            first_name=input.first_name,
            last_name=input.last_name,
            date_joined=input.date_joined,
            last_login=input.last_login,
            is_superuser=input.is_superuser,
            is_staff=input.is_staff,
            is_active=input.is_active,
        )


class DehydrateConta(Mapper[Conta, DjangoUser]):
    @staticmethod
    def map(input: Conta) -> DjangoUser:
        return DjangoUser(
            id=input.id.root,
            username=input.username.root,
            email=input.email.root,
            password=input.password.root,
            is_active=input.is_active,
        )


class OutputToDomainUserMapper(Mapper[ContaOutput, Conta]):
    @staticmethod
    def map(input: ContaOutput) -> Conta:
        return Conta(
            id=input.id,
            username=input.username,
            email=input.email,
            password=input.password,
            is_active=input.is_active,
        )


class OutputToPublicUserMapper(Mapper[ContaOutput, ContaPublic]):
    @staticmethod
    def map(input: ContaOutput) -> ContaPublic:
        return ContaPublic(
            email=input.email,
            username=input.username,
        )


class DomainToOutputUserMapper(Mapper[Conta, ContaOutput]):
    @staticmethod
    def map(input: Conta) -> ContaOutput:
        return ContaOutput(
            id=input.id.root,
            email=input.email.root,
            username=input.username.root,
            password=input.password.root,
            is_active=input.is_active,
        )


class DomainToPublicUserMapper(Mapper[Conta, ContaPublic]):
    @staticmethod
    def map(input: Conta) -> ContaPublic:
        return ContaPublic(
            email=input.email.root,
            username=input.username.root,
        )
