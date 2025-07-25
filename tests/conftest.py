import os
import pytest
from dotenv import load_dotenv
from pathlib import Path
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.app.main import app
from src.infrastructure.sqlalchemy.base import Base

# from src.app.dependencies.user_use_cases import get_sql_user_use_case # NOTE: This file does not exist yet
from src.app.dependencies.category_use_cases import (
    CategoryUseCasesContainer,
    category_container,
)
from src.app.dependencies.product_use_cases import (
    ProductUseCasesContainer,
    product_container,
)

# from src.repositories.sqlalchemy_user_repository import SqlAlchemyUserRepository
from src.repositories.sqlalchemy_category_repository import SqlAlchemyCategoryRepository
from src.repositories.sqlalchemy_product_repository import SqlAlchemyProductRepository

# from src.use_cases.create_user import CreateUserUseCase

# Importa todos los modelos para que Base los conozca
from src.repositories.models import category, product


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


@pytest.fixture(scope="session")
def db_engine():
    """Fixture para crear el motor de la base de datos de prueba una vez por sesión."""
    # Usamos una base de datos en memoria para máxima velocidad
    engine = create_engine(
        "sqlite:///:memory:", connect_args={"check_same_thread": False}
    )
    Base.metadata.create_all(bind=engine)
    yield engine


@pytest.fixture(scope="function")
def db_session(db_engine):
    """
    Fixture que proporciona una sesión de base de datos transaccional para cada test.
    Crea una transacción antes del test y la revierte después, aislando los tests.
    """
    connection = db_engine.connect()
    transaction = connection.begin()
    session = sessionmaker(bind=connection)()

    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()


@pytest.fixture(scope="function")
def category_repository(db_session):
    """Fixture para el repositorio de categorías."""
    return SqlAlchemyCategoryRepository(db_session)


@pytest.fixture(scope="function")
def product_repository(db_session):
    """Fixture para el repositorio de productos."""
    return SqlAlchemyProductRepository(db_session)


# @pytest.fixture
# def override_sql_use_case(sqlite_session):
#     def _override():
#         repo = SqlAlchemyUserRepository(sqlite_session)
#         return CreateUserUseCase(repo)
#
#     app.dependency_overrides[get_sql_user_use_case] = _override
#     yield _override
#     app.dependency_overrides.clear()


@pytest.fixture
def override_product_use_cases(db_session):
    """
    Fixture para sobreescribir los proveedores de casos de uso de productos.
    Crea un contenedor con la sesión de prueba y reemplaza cada método
    del contenedor de producción con el método correspondiente del de prueba.
    """
    test_container = ProductUseCasesContainer(session=db_session)
    app.dependency_overrides[product_container.create_product] = (
        test_container.create_product
    )
    app.dependency_overrides[product_container.get_all_products] = (
        test_container.get_all_products
    )
    app.dependency_overrides[product_container.get_product_by_id] = (
        test_container.get_product_by_id
    )
    app.dependency_overrides[product_container.update_product] = (
        test_container.update_product
    )
    app.dependency_overrides[product_container.delete_product] = (
        test_container.delete_product
    )

    yield
    app.dependency_overrides.clear()


@pytest.fixture
def override_category_use_cases(db_session):
    """
    Fixture para sobreescribir los proveedores de casos de uso de categorías.
    """
    test_container = CategoryUseCasesContainer(session=db_session)
    app.dependency_overrides[category_container.create_category] = (
        test_container.create_category
    )
    app.dependency_overrides[category_container.get_all_categories] = (
        test_container.get_all_categories
    )
    app.dependency_overrides[category_container.get_category_by_id] = (
        test_container.get_category_by_id
    )
    app.dependency_overrides[category_container.update_category] = (
        test_container.update_category
    )
    app.dependency_overrides[category_container.delete_category] = (
        test_container.delete_category
    )

    yield
    app.dependency_overrides.clear()
