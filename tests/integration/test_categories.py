from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from src.app.main import app
from src.repositories.models.product import ProductModel

client = TestClient(app)


def test_create_category_success(override_category_use_cases, db_session: Session):
    """Test creating a category successfully."""
    # Arrange
    category_data = {"name": "Frutas y Verduras", "description": "Productos frescos"}

    # Act
    response = client.post("/v1/categories/", json=category_data)

    # Assert
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == category_data["name"]
    assert "id" in data


def test_create_category_fails_if_name_exists(
    override_category_use_cases, db_session: Session
):
    """Test that creating a category with a duplicate name fails."""
    # Arrange: Create an initial category
    category_data = {"name": "Lácteos", "description": "Leche y derivados"}
    client.post("/v1/categories/", json=category_data)

    # Act: Attempt to create it again
    response = client.post("/v1/categories/", json=category_data)

    # Assert
    assert response.status_code == 409
    assert response.json() == {"detail": "La categoría con este nombre ya existe"}


def test_get_all_categories(override_category_use_cases, db_session: Session):
    """Test getting a list of all categories."""
    # Arrange: Create a couple of categories
    client.post(
        "/v1/categories/", json={"name": "Bebidas", "description": "Refrescos y jugos"}
    )
    client.post(
        "/v1/categories/",
        json={"name": "Snacks", "description": "Papas fritas y otros"},
    )

    # Act
    response = client.get("/v1/categories/")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 2
    assert data[0]["name"] == "Bebidas"
    assert data[1]["name"] == "Snacks"


def test_get_category_by_id_success(override_category_use_cases, db_session: Session):
    """Test getting a single category by its ID successfully."""
    # Arrange
    res = client.post(
        "/v1/categories/", json={"name": "Carnes", "description": "Cortes de carne"}
    )
    category_id = res.json()["id"]

    # Act
    response = client.get(f"/v1/categories/{category_id}")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == category_id
    assert data["name"] == "Carnes"


def test_get_category_by_id_not_found(override_category_use_cases):
    """Test getting a non-existent category returns 404."""
    response = client.get("/v1/categories/9999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Categoría no encontrada"}


def test_update_category_success(override_category_use_cases, db_session: Session):
    """Test updating a category successfully."""
    # Arrange
    res = client.post(
        "/v1/categories/",
        json={"name": "Limpieza Hogar", "description": "Artículos de limpieza"},
    )
    category_id = res.json()["id"]
    update_data = {
        "name": "Limpieza",
        "description": "Artículos de limpieza para el hogar",
    }

    # Act
    response = client.put(f"/v1/categories/{category_id}", json=update_data)

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Limpieza"
    assert data["description"] == "Artículos de limpieza para el hogar"


def test_update_category_name_conflict(
    override_category_use_cases, db_session: Session
):
    """Test updating a category to a name that already exists fails."""
    # Arrange
    client.post("/v1/categories/", json={"name": "Existente"})
    res = client.post("/v1/categories/", json={"name": "A Actualizar"})
    category_id = res.json()["id"]

    # Act
    response = client.put(f"/v1/categories/{category_id}", json={"name": "Existente"})

    # Assert
    assert response.status_code == 409
    assert response.json() == {"detail": "La categoría con este nombre ya existe"}


def test_delete_category_success(override_category_use_cases, db_session: Session):
    """Test deleting a category successfully."""
    # Arrange
    res = client.post("/v1/categories/", json={"name": "A Eliminar"})
    category_id = res.json()["id"]

    # Act
    delete_response = client.delete(f"/v1/categories/{category_id}")

    # Assert
    assert delete_response.status_code == 204
    get_response = client.get(f"/v1/categories/{category_id}")
    assert get_response.status_code == 404


def test_delete_category_with_products_fails(
    override_product_use_cases, override_category_use_cases, db_session: Session
):
    """Test that deleting a category that is in use by products fails."""
    # Arrange
    res = client.post("/v1/categories/", json={"name": "Categoría en Uso"})
    category_id = res.json()["id"]
    client.post(
        "/v1/products/",
        json={
            "name": "Producto 1",
            "sku": "P1",
            "category_id": category_id,
            "cost_price": 1,
            "sale_price": 2,
            "min_stock": 0,
            "max_stock": 10,
            "unit_of_measure": "u",
        },
    )

    # Act
    response = client.delete(f"/v1/categories/{category_id}")

    # Assert
    assert response.status_code == 409
    assert response.json() == {
        "detail": "La categoría está en uso y no puede ser eliminada"
    }
