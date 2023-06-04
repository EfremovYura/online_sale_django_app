from typing import Any
import pytest
from users.models import User


@pytest.mark.django_db
@pytest.fixture
def get_user_data() -> dict[str, str]:
    user_data: dict = {
        "username": "test_username",
        "email": "testemail@test.com",
        "password": "test_password",
        "password_repeat": "test_password",
    }

    return user_data


@pytest.mark.django_db
@pytest.fixture
def updated_user_data(get_authorized_user) -> dict[str, Any]:
    user_data: dict = {
        "id": get_authorized_user.id,
        "username": get_authorized_user.username,
        "first_name": "Ivan",
        "last_name": "Pupkin",
        "email": get_authorized_user.email,
    }

    return user_data


@pytest.mark.django_db
@pytest.fixture
def get_authorized_user(client, django_user_model) -> User:
    user_data: dict = {
        "username": "test_username",
        "email": "testemail@test.com",
        "password": "test_password",
    }

    user: User = django_user_model.objects.create_user(**user_data)

    client.post("/users/login", data=user_data, content_type="application/json")

    return user
