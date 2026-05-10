from typing import Optional

from django.contrib.auth import get_user_model

from rastro.conta.domain.aggregates import Conta
from rastro.conta.domain.repository import ContaRepository
from rastro.conta.domain.value_objects import (
    Email,
    HashedPassword,
    Username,
)
from rastro.conta.presentation.conversions import dehydrate_conta, hydrate_conta
from rastro_shared_kernel.value_objects import Id

DjangoUser = get_user_model()


class DjangoUserRepository(ContaRepository):
    def create(
        self, username: Username, email: Email, password: HashedPassword
    ) -> Conta:
        django_user = DjangoUser.objects.create(
            username=username.root,
            email=email.root,
            password=password.root,
        )
        django_user.save()
        django_user.refresh_from_db()

        return hydrate_conta(django_user)

    def get_by_id(self, id: Id) -> Optional[Conta]:
        try:
            django_user = DjangoUser.objects.get(pk=id.root)

            return hydrate_conta(django_user)
        except DjangoUser.DoesNotExist:
            return None

    def get_by_email(self, email: Email) -> Optional[Conta]:
        try:
            django_user = DjangoUser.objects.get(email=email.root)

            return hydrate_conta(django_user)
        except DjangoUser.DoesNotExist:
            return None

    def get_by_username(self, username: Username) -> Optional[Conta]:
        try:
            django_user = DjangoUser.objects.get(username=username.root)

            django_user.check_password
            return hydrate_conta(django_user)
        except DjangoUser.DoesNotExist:
            return None

    def update_password(self, user: Conta) -> Conta:
        django_user = dehydrate_conta(user)
        django_user.save(update_fields=["password"])

        return hydrate_conta(django_user)
