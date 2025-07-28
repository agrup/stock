from dotenv import load_dotenv
from pathlib import Path
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.app.main import app
from src.infrastructure.sqlalchemy.base import Base
from src.app.dependencies.category_use_cases import (
    CategoryUseCasesContainer,
    category_container,
)
from src.app.dependencies.product_use_cases import (
    ProductUseCasesContainer,
    product_container,
)
from src.app.dependencies.supplier_use_cases import (
    SupplierUseCasesContainer,
    supplier_container,
)
from src.app.dependencies.stock_movement_use_cases import (
    StockMovementUseCasesContainer,
    stock_movement_container,
)


@pytest.fixture(scope="session", autouse=True)
def load_test_env():
    env_path = Path(".env.test")
    if env_path.exists():
        load_dotenv(dotenv_path=env_path, override=True)
    else:
        pass


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
    overrides = {
        product_container.create_product: test_container.create_product,
        product_container.get_all_products: test_container.get_all_products,
        product_container.get_product_by_id: test_container.get_product_by_id,
        product_container.update_product: test_container.update_product,
        product_container.delete_product: test_container.delete_product,
    }
    app.dependency_overrides.update(overrides)

    yield
    app.dependency_overrides.clear()


@pytest.fixture
def override_stock_movement_use_cases(db_session):
    """
    Fixture para sobreescribir los proveedores de casos de uso de movimientos de stock.
    """
    test_container = StockMovementUseCasesContainer(session=db_session)
    overrides = {
        stock_movement_container.create_stock_movement: test_container.create_stock_movement,
    }
    app.dependency_overrides.update(overrides)

    yield
    app.dependency_overrides.clear()


@pytest.fixture
def override_supplier_use_cases(db_session):
    """
    Fixture para sobreescribir los proveedores de casos de uso de proveedores.
    """
    test_container = SupplierUseCasesContainer(session=db_session)
    overrides = {
        supplier_container.create_supplier: test_container.create_supplier,
        supplier_container.get_all_suppliers: test_container.get_all_suppliers,
        supplier_container.get_supplier_by_id: test_container.get_supplier_by_id,
        supplier_container.update_supplier: test_container.update_supplier,
        supplier_container.delete_supplier: test_container.delete_supplier,
    }
    app.dependency_overrides.update(overrides)

    yield
    app.dependency_overrides.clear()


@pytest.fixture
def override_category_use_cases(db_session):
    """
    Fixture para sobreescribir los proveedores de casos de uso de categorías.
    """
    test_container = CategoryUseCasesContainer(session=db_session)
    overrides = {
        category_container.create_category: test_container.create_category,
        category_container.get_all_categories: test_container.get_all_categories,
        category_container.get_category_by_id: test_container.get_category_by_id,
        category_container.update_category: test_container.update_category,
        category_container.delete_category: test_container.delete_category,
    }
    app.dependency_overrides.update(overrides)

    yield
    app.dependency_overrides.clear()
