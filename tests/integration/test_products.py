from fastapi.testclient import TestClient
from src.app.main import app

client = TestClient(app)


def test_create_product_success(override_create_product_use_case):
    """Test creating a product successfully."""
    product_data = {
        "name": "Producto de Prueba",
        "sku": "SKU12345",
        "description": "Un producto para testing",
        "unit_of_measure": "unidad",
        "cost_price": 10.50,
        "sale_price": 15.75,
        "min_stock": 5,
        "max_stock": 50,
        "category_id": 1,
    }
    response = client.post("/v1/products", json=product_data)
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
    response = client.post("/v1/products", json=product_data)
    assert response.status_code == 404
    assert response.json() == {"detail": "La categoría especificada no existe"}
