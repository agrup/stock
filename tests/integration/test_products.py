from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from src.app.main import app
from src.repositories.models.category import CategoryModel
from src.repositories.models.product import ProductModel

client = TestClient(app)


def test_create_product_success(override_product_use_cases, override_category_use_cases, db_session: Session):
    """Test creating a product successfully."""
    # Arrange: Create a category using the API
    res_cat = client.post(
        "/v1/categories/", json={"name": "Electrónica", "description": "Dispositivos electrónicos"}
    )
    assert res_cat.status_code == 201

    product_data = {
        "name": "Producto de Prueba",
        "sku": "SKU12345",
        "description": "Un producto para testing",
        "unit_of_measure": "unidad",
        "cost_price": 10.50,
        "sale_price": 15.75,
        "min_stock": 5,
        "max_stock": 50,
        "category_id": res_cat.json()["id"],
    }
    # Act
    response = client.post("/v1/products/", json=product_data)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == product_data["name"]
    assert data["sku"] == product_data["sku"]
    assert "id" in data


def test_create_product_fails_if_category_not_found(override_product_use_cases):
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


def test_create_product_fails_if_supplier_not_found(
    override_product_use_cases, override_category_use_cases, db_session: Session
):
    """Test that product creation fails with a 404 if the supplier does not exist."""
    # Arrange: Create a category first
    res_cat = client.post(
        "/v1/categories/", json={"name": "Cat for Supplier Test", "description": ""}
    )
    assert res_cat.status_code == 201

    product_data = {
        "name": "Producto con Proveedor Fantasma",
        "sku": "SKU-FAIL-SUP-404",
        "unit_of_measure": "unidad",
        "cost_price": 10.0,
        "sale_price": 20.0,
        "min_stock": 1,
        "max_stock": 10,
        "category_id": res_cat.json()["id"],
        "supplier_id": 9999,  # ID de proveedor que no existe
    }
    # Act
    response = client.post("/v1/products/", json=product_data)

    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": "El proveedor especificado no existe"}


def test_create_product_fails_if_sku_exists(
    override_product_use_cases, override_category_use_cases, db_session: Session
):
    """Test that product creation fails with a 409 if the SKU already exists."""
    # Arrange: Create a category and an initial product
    res_cat = client.post(
        "/v1/categories/", json={"name": "Ropa", "description": "Prendas de vestir"}
    )
    assert res_cat.status_code == 201

    initial_product_data = {
        "name": "Camiseta Original",
        "sku": "SKU-DUPLICADO-123",
        "description": "Una camiseta de algodón",
        "unit_of_measure": "unidad",
        "cost_price": 8.0,
        "sale_price": 12.0,
        "min_stock": 10,
        "max_stock": 100,
        "category_id": res_cat.json()["id"],
    }
    client.post("/v1/products/", json=initial_product_data)

    # Act: Attempt to create another product with the same SKU
    response = client.post("/v1/products/", json=initial_product_data)

    # Assert
    assert response.status_code == 409
    assert response.json() == {"detail": "El producto con este SKU ya existe"}


def test_get_all_products(
    override_product_use_cases,
    override_category_use_cases,
    db_session: Session,
):
    """Test getting a list of all products."""
    # Arrange: Create a category and a product using the POST endpoint
    res_cat = client.post("/v1/categories/", json={"name": "Bebidas", "description": "Líquidos para beber"})
    assert res_cat.status_code == 201

    product_data = {
        "name": "Refresco de Cola",
        "sku": "RC-001",
        "unit_of_measure": "lata",
        "cost_price": 0.5,
        "sale_price": 1.0,
        "min_stock": 20,
        "max_stock": 200,
        "category_id": res_cat.json()["id"],
    }
    client.post("/v1/products/", json=product_data)

    # Act
    response = client.get("/v1/products/")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["name"] == product_data["name"]
    assert data[0]["sku"] == product_data["sku"]


def test_get_product_by_id_success(
    override_product_use_cases,
    override_category_use_cases,
    db_session: Session,
):
    """Test getting a single product by its ID successfully."""
    # Arrange: Create a category and a product via API
    res_cat = client.post("/v1/categories/", json={"name": "Herramientas", "description": "Herramientas manuales"})
    assert res_cat.status_code == 201
    product_data = {
        "name": "Martillo", "sku": "MAR-001", "category_id": res_cat.json()["id"],
        "unit_of_measure": "unidad", "cost_price": 12.0, "sale_price": 20.0,
        "min_stock": 5, "max_stock": 25,
    }
    res_prod = client.post("/v1/products/", json=product_data)
    assert res_prod.status_code == 201
    product_id = res_prod.json()["id"]

    # Act
    response = client.get(f"/v1/products/{product_id}")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == product_id
    assert data["name"] == "Martillo"
    assert data["sku"] == "MAR-001"


def test_get_product_by_id_not_found(override_product_use_cases):
    """Test getting a non-existent product returns 404."""
    response = client.get("/v1/products/9999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Producto no encontrado"}


def test_update_product_success(override_product_use_cases, override_category_use_cases, db_session: Session):
    """Test updating a product successfully."""
    # Arrange: Create a category and a product via API
    res_cat = client.post("/v1/categories/", json={"name": "Lácteos", "description": "Productos lácteos"})
    assert res_cat.status_code == 201
    product_data = {
        "name": "Leche Entera", "sku": "LE-001", "category_id": res_cat.json()["id"],
        "unit_of_measure": "litro", "cost_price": 0.8, "sale_price": 1.2,
        "min_stock": 10, "max_stock": 50,
    }
    res_prod = client.post("/v1/products/", json=product_data)
    assert res_prod.status_code == 201
    product_id = res_prod.json()["id"]

    update_data = {"name": "Leche Entera (1L)", "sale_price": 1.25}

    # Act
    response = client.put(f"/v1/products/{product_id}", json=update_data)

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Leche Entera (1L)"
    assert data["sale_price"] == 1.25
    assert data["sku"] == "LE-001"  # SKU should not change if not provided


def test_update_product_not_found(override_product_use_cases):
    """Test that updating a non-existent product returns 404."""
    response = client.put("/v1/products/9999", json={"name": "Producto Fantasma"})
    assert response.status_code == 404
    assert response.json() == {"detail": "Producto no encontrado"}


def test_update_product_sku_conflict(override_product_use_cases, override_category_use_cases, db_session: Session):
    """Test that updating a product's SKU to an existing one fails."""
    # Arrange
    res_cat = client.post(
        "/v1/categories/", json={"name": "General", "description": ""}
    )
    assert res_cat.status_code == 201
    # Create product 1
    client.post(
        "/v1/products/",
        json={
            "name": "Producto 1",
            "sku": "SKU-EXISTENTE",
            "category_id": res_cat.json()["id"],
            "cost_price": 1,
            "sale_price": 2,
            "min_stock": 0,
            "max_stock": 10,
            "unit_of_measure": "u",
        },
    )
    # Create product 2
    res = client.post(
        "/v1/products/",
        json={
            "name": "Producto 2",
            "sku": "SKU-A-CAMBIAR",
            "category_id": res_cat.json()["id"],
            "cost_price": 1,
            "sale_price": 2,
            "min_stock": 0,
            "max_stock": 10,
            "unit_of_measure": "u",
        },
    )
    product2_id = res.json()["id"]

    # Act: Try to update product 2's SKU to product 1's SKU
    response = client.put(f"/v1/products/{product2_id}", json={"sku": "SKU-EXISTENTE"})

    # Assert
    assert response.status_code == 409
    assert response.json() == {"detail": "El producto con este SKU ya existe"}


def test_delete_product_success(override_product_use_cases, override_category_use_cases, db_session: Session):
    """Test deleting a product successfully."""
    # Arrange: Create a category and a product via API
    res_cat = client.post("/v1/categories/", json={"name": "Congelados", "description": "Productos congelados"})
    assert res_cat.status_code == 201
    product_data = {
        "name": "Helado de Vainilla", "sku": "HV-001", "category_id": res_cat.json()["id"],
        "unit_of_measure": "litro", "cost_price": 2.0, "sale_price": 4.5,
        "min_stock": 5, "max_stock": 20,
    }
    res_prod = client.post("/v1/products/", json=product_data)
    assert res_prod.status_code == 201
    product_id = res_prod.json()["id"]

    # Act
    delete_response = client.delete(f"/v1/products/{product_id}")

    # Assert
    assert delete_response.status_code == 204

    # Verify it's gone
    get_response = client.get(f"/v1/products/{product_id}")
    assert get_response.status_code == 404


def test_delete_product_not_found(override_product_use_cases):
    """Test that deleting a non-existent product returns 404."""
    response = client.delete("/v1/products/9999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Producto no encontrado"}
