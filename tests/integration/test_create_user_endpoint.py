from fastapi.testclient import TestClient
import pytest

from src.app.main import app
from src.use_cases.create_user import CreateUserUseCase
from src.repositories.sqlalchemy_user_repository import SqlAlchemyUserRepository
from src.app.dependencies.user_use_cases import get_sql_user_use_case

client = TestClient(app)


@pytest.fixture
def override_sql_use_case(sqlite_session):
    def override():
        return CreateUserUseCase(SqlAlchemyUserRepository(sqlite_session))

    app.dependency_overrides[get_sql_user_use_case] = override
    yield
    app.dependency_overrides.clear()


def test_create_user_endpoint_sql(override_sql_use_case):
    payload = {"name": "Agustin Ro", "email": "agus@example.com"}
    response = client.post("/v1/users", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Agustin Ro"
    assert data["email"] == "agus@example.com"
    assert data["id"] == 1
