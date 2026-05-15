from django.contrib.auth.models import User

from rastro.conta.domain.value_objects import Email, Username
from rastro.conta.presentation.mappers import DehydrateContaMapper, HydrateContaMapper


def test_hydrate_conta(user: User) -> None:
    conta = HydrateContaMapper.map(user)

    assert conta.username == Username(user.username)
    assert conta.email == Email(user.email)
    assert conta.first_name == user.first_name
    assert conta.last_name == user.last_name
    assert conta.date_joined == user.date_joined
    assert conta.last_login == user.last_login
    assert conta.is_active == user.is_active
    assert conta.is_staff == user.is_staff
    assert conta.is_superuser == user.is_superuser


def test_dehydrate_conta(user: User) -> None:
    dehydrated_user = DehydrateContaMapper.map(HydrateContaMapper.map(user))

    assert dehydrated_user.username == user.username
    assert dehydrated_user.email == user.email
    assert dehydrated_user.first_name == user.first_name
    assert dehydrated_user.last_name == user.last_name
    assert dehydrated_user.date_joined == user.date_joined
    assert dehydrated_user.last_login == user.last_login
    assert dehydrated_user.is_active == user.is_active
    assert dehydrated_user.is_staff == user.is_staff
    assert dehydrated_user.is_superuser == user.is_superuser
