from abc import ABC, abstractmethod

from django.contrib.auth.models import User as DjangoUser

from rastro.users.entities import User
from rastro.users.mappers import DjangoUserModelToEntityMapper


class UserRepository(ABC):
    @abstractmethod
    def get_by_id(self, id: int) -> User | None: ...

    @abstractmethod
    def get_by_email(self, email: str) -> User | None: ...

    @abstractmethod
    def get_by_username(self, username: str) -> User | None: ...

    @abstractmethod
    def save(self, user: User) -> User: ...


class DjangoUserRepository(UserRepository):
    def get_by_id(self, id: int) -> User | None:
        try:
            user = DjangoUser.objects.get(pk=id)  # type: ignore[misc]

            return DjangoUserModelToEntityMapper.map(user)
        except DjangoUser.DoesNotExist:
            return None

    def get_by_email(self, email: str) -> User | None:
        try:
            user = DjangoUser.objects.get(email=email)  # type: ignore[misc]

            return DjangoUserModelToEntityMapper.map(user)
        except DjangoUser.DoesNotExist:
            return None

    def get_by_username(self, username: str) -> User | None:
        try:
            user = DjangoUser.objects.get(username=username)  # type: ignore[misc]

            return DjangoUserModelToEntityMapper.map(user)
        except DjangoUser.DoesNotExist:
            return None

    def save(self, user: User) -> User:
        if user.id is None:
            inner_user = DjangoUser.objects.create_user(  # type: ignore[misc]
                username=user.username.value,
                email=user.email.value,
                password=user.password.value,
            )

            return DjangoUserModelToEntityMapper.map(inner_user)

        inner_user = DjangoUser.objects.get(pk=user.id.value)  # type: ignore[misc]

        inner_user.username = user.username.value
        inner_user.email = user.email.value
        inner_user.password = user.password.value

        inner_user.save()

        return DjangoUserModelToEntityMapper.map(inner_user)
