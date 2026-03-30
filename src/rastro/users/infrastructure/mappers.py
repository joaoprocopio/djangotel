from django.contrib.auth.models import User as DjangoUser

from rastro.base.entity import Id
from rastro.base.mapper import Mapper
from rastro.users.domain.user import User
from rastro.users.domain.value_objects import Email, HashedPassword, Username


class DjangoUserToDomainMapper(Mapper[DjangoUser, User]):
    @staticmethod
    def map(input: DjangoUser) -> User:
        return User(
            id=Id(input.pk),
            username=Username(input.username),
            email=Email(input.email),
            hashed_password=HashedPassword(input.password),
            is_active=input.is_active,
            is_verified=input.is_active,
        )


class DomainUserToOutputMapper(Mapper[User, dict[str, object]]):
    @staticmethod
    def map(input: User) -> dict[str, object]:
        return {
            "id": input.id.value,
            "username": input.username.value,
            "email": input.email.value,
            "is_active": input.is_active,
            "is_verified": input.is_verified,
        }
