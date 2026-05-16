from django.contrib.auth.models import User

from rastro.conta.domain.value_objects import Email, Username
from rastro.conta.shared.mappers import (
    DehydrateContaMapper,
    HydrateContaMapper,
    OutputContaMapper,
    PresentContaMapper,
)


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
    conta = DehydrateContaMapper.map(HydrateContaMapper.map(user))

    assert conta.username == user.username
    assert conta.email == user.email
    assert conta.first_name == user.first_name
    assert conta.last_name == user.last_name
    assert conta.date_joined == user.date_joined
    assert conta.last_login == user.last_login
    assert conta.is_active == user.is_active
    assert conta.is_staff == user.is_staff
    assert conta.is_superuser == user.is_superuser


def test_preset_conta_from_domain(user: User) -> None:
    conta = HydrateContaMapper.map(user)
    conta_public = PresentContaMapper.map(conta)

    assert conta.email == conta_public.email
    assert conta.username == conta_public.username


def test_preset_conta_from_output(user: User) -> None:
    conta = HydrateContaMapper.map(user)
    conta_output = OutputContaMapper.map(conta)
    conta_public = PresentContaMapper.map(conta_output)

    assert conta.email == conta_public.email
    assert conta.username == conta_public.username


def test_output_conta(user: User) -> None:
    conta = HydrateContaMapper.map(user)
    conta_output = OutputContaMapper.map(conta)

    assert conta.username == conta_output.username
    assert conta.email == conta_output.email
    assert conta.first_name == conta_output.first_name
    assert conta.last_name == conta_output.last_name
    assert conta.date_joined == conta_output.date_joined
    assert conta.last_login == conta_output.last_login
    assert conta.is_active == conta_output.is_active
    assert conta.is_staff == conta_output.is_staff
    assert conta.is_superuser == conta_output.is_superuser
