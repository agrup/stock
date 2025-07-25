from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from src.app.main import app

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


def test_create_category_fails_if_name_exists(override_category_use_cases, db_session: Session):
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
    client.post("/v1/categories/", json={"name": "Bebidas", "description": "Refrescos y jugos"})
    client.post("/v1/categories/", json={"name": "Snacks", "description": "Papas fritas y otros"})

    # Act
    response = client.get("/v1/categories/")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 2
    assert data[0]["name"] == "Bebidas"
    assert data[1]["name"] == "Snacks"