from typing import Optional

from django.contrib.auth import get_user_model

from rastro.auth.domain.aggregates import User
from rastro.auth.domain.repository import UserRepository
from rastro.auth.domain.value_objects import (
    Email,
    HashedPassword,
    Username,
)
from rastro.auth.infrastructure.mappers import DjangoToDomainUserMapper
from rastro_shared_kernel.value_objects import Id

DjangoUser = get_user_model()


class DjangoUserRepository(UserRepository):
    def create(
        self, username: Username, email: Email, password: HashedPassword
    ) -> User:
        django_user = DjangoUser.objects.create(
            username=username.root,
            email=email.root,
            password=password.root,
        )
        django_user.save()
        django_user.refresh_from_db()

        return DjangoToDomainUserMapper.map(django_user)

    def get_by_id(self, id: Id) -> Optional[User]:
        try:
            django_user = DjangoUser.objects.get(pk=id.root)

            return DjangoToDomainUserMapper.map(django_user)
        except DjangoUser.DoesNotExist:
            return None

    def get_by_email(self, email: Email) -> Optional[User]:
        try:
            django_user = DjangoUser.objects.get(email=email.root)

            return DjangoToDomainUserMapper.map(django_user)
        except DjangoUser.DoesNotExist:
            return None

    def get_by_username(self, username: Username) -> Optional[User]:
        try:
            django_user = DjangoUser.objects.get(username=username.root)

            return DjangoToDomainUserMapper.map(django_user)
        except DjangoUser.DoesNotExist:
            return None
