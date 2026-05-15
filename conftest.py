import pytest
from django.contrib.auth.models import AnonymousUser, User
from model_bakery import baker


@pytest.fixture
def user(db: None) -> User:
    username = "username"
    password = "password"

    user = baker.make(
        User,
        username=username,
        first_name="Test",
        last_name="User",
        email=f"{username}@email.com",
    )
    user.set_password(password)
    user.save()

    return user


@pytest.fixture
def anonymous_user(db: None) -> AnonymousUser:
    return AnonymousUser()
