import os
import pytest
from dotenv import load_dotenv
from pathlib import Path
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.app.main import app
from src.infrastructure.sqlalchemy.base import Base
from src.repositories.models.users import UserModel
from src.app.dependencies.user_use_cases import get_sql_user_use_case
from src.repositories.sqlalchemy_user_repository import SqlAlchemyUserRepository
from src.use_cases.create_user import (
    CreateUserUseCase,
)  # asegurate de importar modelos usados


@pytest.fixture(scope="session", autouse=True)
def load_test_env():
    env_path = Path(".env.test")
    if env_path.exists():
        load_dotenv(dotenv_path=env_path, override=True)
        print(f"[pytest] ✅ Variables de entorno cargadas desde {env_path}")
    else:
        print(
            f"[pytest] ⚠️ Archivo {env_path} no encontrado. Se omite la carga de entorno."
        )


@pytest.fixture(scope="function")
def sqlite_session():
    engine = create_engine(
        "sqlite:///./test.db", connect_args={"check_same_thread": False}
    )

    Base.metadata.create_all(bind=engine)

    TestingSessionLocal = sessionmaker(bind=engine)

    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        os.remove("./test.db")


@pytest.fixture
def override_sql_use_case(sqlite_session):
    def _override():
        repo = SqlAlchemyUserRepository(sqlite_session)
        return CreateUserUseCase(repo)

    app.dependency_overrides[get_sql_user_use_case] = _override
    yield _override
    app.dependency_overrides.clear()
