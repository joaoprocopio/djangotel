import pytest
from django.contrib.auth.models import AnonymousUser
from model_bakery import baker

from rastro.conta.models import Conta


@pytest.fixture
def conta(db: None) -> Conta:
    conta = baker.make(
        Conta,
        display_name="Test User",
        email="testuser@email.com",
    )
    conta.set_password("password")
    conta.save()

    return conta


@pytest.fixture
def anonymous_user(db: None) -> AnonymousUser:
    return AnonymousUser()
