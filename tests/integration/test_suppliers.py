from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from src.app.main import app

client = TestClient(app)


def test_create_supplier_success(override_supplier_use_cases, db_session: Session):
    """Test creating a supplier successfully."""
    # Arrange
    supplier_data = {
        "name": "Proveedor A",
        "contact_person": "Juan Pérez",
        "email": "juan.perez@proveedora.com",
        "phone": "123456789",
    }

    # Act
    response = client.post("/v1/suppliers/", json=supplier_data)

    # Assert
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == supplier_data["name"]
    assert data["email"] == supplier_data["email"]
    assert "id" in data


def test_create_supplier_fails_if_name_exists(
    override_supplier_use_cases, db_session: Session
):
    """Test that creating a supplier with a duplicate name fails."""
    # Arrange
    supplier_data = {"name": "Proveedor Duplicado"}
    client.post("/v1/suppliers/", json=supplier_data)

    # Act
    response = client.post("/v1/suppliers/", json=supplier_data)

    # Assert
    assert response.status_code == 409
    assert response.json() == {"detail": "El proveedor con este nombre ya existe"}


def test_get_all_suppliers(override_supplier_use_cases, db_session: Session):
    """Test getting a list of all suppliers."""
    # Arrange
    client.post("/v1/suppliers/", json={"name": "Proveedor 1"})
    client.post("/v1/suppliers/", json={"name": "Proveedor 2"})

    # Act
    response = client.get("/v1/suppliers/")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 2
    assert data[0]["name"] == "Proveedor 1"
    assert data[1]["name"] == "Proveedor 2"


def test_get_supplier_by_id_success(override_supplier_use_cases, db_session: Session):
    """Test getting a single supplier by its ID successfully."""
    # Arrange
    res = client.post("/v1/suppliers/", json={"name": "Proveedor B"})
    supplier_id = res.json()["id"]

    # Act
    response = client.get(f"/v1/suppliers/{supplier_id}")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == supplier_id
    assert data["name"] == "Proveedor B"


def test_update_supplier_success(override_supplier_use_cases, db_session: Session):
    """Test updating a supplier successfully."""
    # Arrange
    res = client.post("/v1/suppliers/", json={"name": "Proveedor C"})
    supplier_id = res.json()["id"]
    update_data = {"contact_person": "Ana García", "phone": "987654321"}

    # Act
    response = client.put(f"/v1/suppliers/{supplier_id}", json=update_data)

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["contact_person"] == "Ana García"
    assert data["phone"] == "987654321"
    assert data["name"] == "Proveedor C"  # Name should not change


def test_update_supplier_not_found(override_supplier_use_cases):
    """Test that updating a non-existent supplier returns 404."""
    response = client.put("/v1/suppliers/9999", json={"name": "Fantasma"})
    assert response.status_code == 404
    assert response.json() == {"detail": "Proveedor no encontrado"}


def test_update_supplier_name_conflict(
    override_supplier_use_cases, db_session: Session
):
    """Test updating a supplier to a name that already exists fails."""
    # Arrange
    client.post("/v1/suppliers/", json={"name": "Proveedor Existente"})
    res = client.post("/v1/suppliers/", json={"name": "Proveedor a Actualizar"})
    supplier_id = res.json()["id"]

    # Act
    response = client.put(
        f"/v1/suppliers/{supplier_id}", json={"name": "Proveedor Existente"}
    )

    # Assert
    assert response.status_code == 409
    assert response.json() == {"detail": "El proveedor con este nombre ya existe"}


def test_delete_supplier_success(override_supplier_use_cases, db_session: Session):
    """Test deleting a supplier successfully."""
    # Arrange
    res = client.post("/v1/suppliers/", json={"name": "Proveedor a Eliminar"})
    supplier_id = res.json()["id"]

    # Act
    delete_response = client.delete(f"/v1/suppliers/{supplier_id}")

    # Assert
    assert delete_response.status_code == 204

    # Verify it's gone
    get_response = client.get(f"/v1/suppliers/{supplier_id}")
    assert get_response.status_code == 404


def test_delete_supplier_not_found(override_supplier_use_cases):
    """Test that deleting a non-existent supplier returns 404."""
    response = client.delete("/v1/suppliers/9999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Proveedor no encontrado"}


def test_delete_supplier_with_products_fails(
    override_product_use_cases,
    override_supplier_use_cases,
    override_category_use_cases,
    db_session: Session,
):
    """Test that deleting a supplier that is in use by products fails."""
    # Arrange
    # 1. Create a category
    cat_res = client.post("/v1/categories/", json={"name": "Test Category for Supplier"})
    category_id = cat_res.json()["id"]

    # 2. Create a supplier
    sup_res = client.post("/v1/suppliers/", json={"name": "Supplier in Use"})
    supplier_id = sup_res.json()["id"]

    # 3. Create a product linked to the supplier
    client.post(
        "/v1/products/",
        json={
            "name": "Producto Linked to Supplier",
            "sku": "P1-SUP-LINK",
            "category_id": category_id,
            "supplier_id": supplier_id,
            "cost_price": 1,
            "sale_price": 2,
            "min_stock": 0,
            "max_stock": 10,
            "unit_of_measure": "u",
        },
    )

    # Act
    response = client.delete(f"/v1/suppliers/{supplier_id}")

    # Assert
    assert response.status_code == 409
    assert response.json() == {
        "detail": "El proveedor está en uso y no puede ser eliminado"
    }