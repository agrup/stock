from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from src.app.main import app
from src.repositories.models.category import CategoryModel

client = TestClient(app)


def test_create_product_success(
    override_create_product_use_case, sqlite_session: Session
):
    """Test creating a product successfully."""
    # Arrange: Primero, creamos una categoría para que el producto pueda asociarse a ella.
    category = CategoryModel(name="Electrónica", description="Dispositivos electrónicos")
    sqlite_session.add(category)
    sqlite_session.commit()

    product_data = {
        "name": "Producto de Prueba",
        "sku": "SKU12345",
        "description": "Un producto para testing",
        "unit_of_measure": "unidad",
        "cost_price": 10.50,
        "sale_price": 15.75,
        "min_stock": 5,
        "max_stock": 50,
        "category_id": category.id,
    }
    # Act
    response = client.post("/v1/products/", json=product_data)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == product_data["name"]
    assert data["sku"] == product_data["sku"]
    assert "id" in data

def test_create_product_fails_if_category_not_found(override_create_product_use_case):
    """Test that product creation fails with a 404 if the category does not exist."""
    product_data = {
        "name": "Producto Fallido",
        "sku": "SKU-FAIL-404",
        "description": "Un producto cuya categoría no existe",
        "unit_of_measure": "unidad",
        "cost_price": 10.0,
        "sale_price": 20.0,
        "min_stock": 1,
        "max_stock": 10,
        "category_id": 999,  # ID de categoría que no existe
    }
    response = client.post("/v1/products/", json=product_data)
    assert response.status_code == 404
    assert response.json() == {"detail": "La categoría especificada no existe"}


def test_create_product_fails_if_sku_exists(
    override_create_product_use_case, sqlite_session: Session
):
    """Test that product creation fails with a 409 if the SKU already exists."""
    # Arrange: Create a category and an initial product
    category = CategoryModel(name="Ropa", description="Prendas de vestir")
    sqlite_session.add(category)
    sqlite_session.commit()

    initial_product_data = {
        "name": "Camiseta Original",
        "sku": "SKU-DUPLICADO-123",
        "description": "Una camiseta de algodón",
        "unit_of_measure": "unidad",
        "cost_price": 8.0,
        "sale_price": 12.0,
        "min_stock": 10,
        "max_stock": 100,
        "category_id": category.id,
    }
    client.post("/v1/products/", json=initial_product_data)

    # Act: Attempt to create another product with the same SKU
    response = client.post("/v1/products/", json=initial_product_data)

    # Assert
    assert response.status_code == 409
    assert response.json() == {"detail": "El producto con este SKU ya existe"}
