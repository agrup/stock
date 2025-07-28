from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from src.app.main import app
from src.repositories.models.product import ProductModel

client = TestClient(app)


def test_create_stock_entry_success(
    override_product_use_cases,
    override_category_use_cases,
    override_stock_movement_use_cases,
    db_session: Session,
):
    """Test creating a stock entry ('ENTRADA') successfully."""
    # Arrange: Create a product with initial stock 0
    res_cat = client.post("/v1/categories/", json={"name": "Category A"})
    product_data = {
        "name": "Producto A", "sku": "SKU-A", "category_id": res_cat.json()["id"],
        "cost_price": 10, "sale_price": 20, "min_stock": 5, "max_stock": 100,
        "unit_of_measure": "unidad",
    }
    res_prod = client.post("/v1/products/", json=product_data)
    assert res_prod.status_code == 201, f"Failed to create product: {res_prod.text}"
    product_id = res_prod.json()["id"]
    assert res_prod.json()["current_stock"] == 0

    movement_data = {
        "product_id": product_id,
        "movement_type": "ENTRADA",
        "quantity": 50,
        "reason": "Compra inicial",
    }

    # Act
    response = client.post("/v1/stock-movements/", json=movement_data)

    # Assert: Check movement creation and stock update
    assert response.status_code == 201
    movement_res = response.json()
    assert movement_res["product_id"] == product_id
    assert movement_res["quantity"] == 50

    # Verify that the product's stock has been updated
    product_res = client.get(f"/v1/products/{product_id}")
    assert product_res.json()["current_stock"] == 50


def test_create_stock_exit_success(
    override_product_use_cases,
    override_category_use_cases,
    override_stock_movement_use_cases,
    db_session: Session,
):
    """Test creating a stock exit ('SALIDA') successfully."""
    # Arrange: Create a product and add 100 units of stock
    res_cat = client.post("/v1/categories/", json={"name": "Category B"})
    product_data = {
        "name": "Producto B", "sku": "SKU-B", "category_id": res_cat.json()["id"],
        "cost_price": 10, "sale_price": 20, "min_stock": 5, "max_stock": 100,
        "unit_of_measure": "unidad",
    }
    res_prod = client.post("/v1/products/", json=product_data)
    assert res_prod.status_code == 201, f"Failed to create product: {res_prod.text}"
    product_id = res_prod.json()["id"]
    # Add initial stock
    client.post("/v1/stock-movements/", json={"product_id": product_id, "movement_type": "ENTRADA", "quantity": 100})

    movement_data = {
        "product_id": product_id,
        "movement_type": "SALIDA",
        "quantity": 30,
        "reason": "Venta a cliente",
    }

    # Act
    response = client.post("/v1/stock-movements/", json=movement_data)

    # Assert
    assert response.status_code == 201
    product_res = client.get(f"/v1/products/{product_id}")
    assert product_res.json()["current_stock"] == 70  # 100 - 30


def test_create_stock_adjustment_success(
    override_product_use_cases,
    override_category_use_cases,
    override_stock_movement_use_cases,
    db_session: Session,
):
    """Test creating a stock adjustment ('AJUSTE') successfully."""
    # Arrange: Create a product and add 88 units of stock
    res_cat = client.post("/v1/categories/", json={"name": "Category C"})
    product_data = {
        "name": "Producto C", "sku": "SKU-C", "category_id": res_cat.json()["id"],
        "cost_price": 10, "sale_price": 20, "min_stock": 5, "max_stock": 100,
        "unit_of_measure": "unidad",
    }
    res_prod = client.post("/v1/products/", json=product_data)
    assert res_prod.status_code == 201, f"Failed to create product: {res_prod.text}"
    product_id = res_prod.json()["id"]
    client.post("/v1/stock-movements/", json={"product_id": product_id, "movement_type": "ENTRADA", "quantity": 88})

    movement_data = {
        "product_id": product_id,
        "movement_type": "AJUSTE",
        "quantity": 75,  # The new total stock
        "reason": "Recuento de inventario",
    }

    # Act
    response = client.post("/v1/stock-movements/", json=movement_data)

    # Assert
    assert response.status_code == 201
    product_res = client.get(f"/v1/products/{product_id}")
    assert product_res.json()["current_stock"] == 75  # Stock is set to the new value


def test_create_stock_exit_fails_if_insufficient_stock(
    override_product_use_cases,
    override_category_use_cases,
    override_stock_movement_use_cases,
    db_session: Session,
):
    """Test that a 'SALIDA' fails if there is not enough stock."""
    # Arrange: Create a product and add 10 units of stock
    res_cat = client.post("/v1/categories/", json={"name": "Category D"})
    product_data = {
        "name": "Producto D", "sku": "SKU-D", "category_id": res_cat.json()["id"],
        "cost_price": 10, "sale_price": 20, "min_stock": 5, "max_stock": 100,
        "unit_of_measure": "unidad",
    }
    res_prod = client.post("/v1/products/", json=product_data)
    assert res_prod.status_code == 201, f"Failed to create product: {res_prod.text}"
    product_id = res_prod.json()["id"]
    client.post("/v1/stock-movements/", json={"product_id": product_id, "movement_type": "ENTRADA", "quantity": 10})

    movement_data = {
        "product_id": product_id,
        "movement_type": "SALIDA",
        "quantity": 11,  # More than available
    }

    # Act
    response = client.post("/v1/stock-movements/", json=movement_data)

    # Assert
    assert response.status_code == 409
    assert response.json() == {"detail": "Stock insuficiente para realizar la operación"}