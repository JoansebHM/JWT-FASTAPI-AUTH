import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.models import User as UserModel
from app.core.security import get_current_user
from app.core.security import list_users


@pytest.fixture
def client():
    return TestClient(app)


def fake_user():
    return UserModel(
        id=1,
        email="test@test.com",
        full_name="Test User",
        is_active=True,
        user_type="user",
    )


def fake_users():
    return [
        UserModel(
            id=1,
            email="a@test.com",
            full_name="user A",
            is_active=True,
            user_type="user",
        ),
        UserModel(
            id=2,
            email="b@test.com",
            full_name="user B",
            is_active=True,
            user_type="user",
        ),
    ]


@pytest.fixture(autouse=True)
def override_dependencies():
    app.dependency_overrides[get_current_user] = fake_user
    app.dependency_overrides[list_users] = fake_users

    yield

    app.dependency_overrides = {}
