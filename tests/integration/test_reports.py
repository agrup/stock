from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from src.app.main import app

client = TestClient(app)


def test_get_low_stock_report(
    override_product_use_cases,
    override_category_use_cases,
    override_stock_movement_use_cases,
    db_session: Session,
):
    """Test the low stock products report endpoint."""
    # Arrange: Create a category and several products
    res_cat = client.post("/v1/categories/", json={"name": "Low Stock Category"})
    category_id = res_cat.json()["id"]

    # Product 1: Low stock (current < min)
    res_p1 = client.post("/v1/products/", json={
        "name": "Producto Bajo Stock", "sku": "LOW1", "category_id": category_id,
        "cost_price": 10, "sale_price": 20, "min_stock": 10, "max_stock": 100,
        "unit_of_measure": "u", 
    })
    p1_id = res_p1.json()["id"]
    # Set stock to 5 using a stock movement
    client.post("/v1/stock-movements/", json={"product_id": p1_id, "movement_type": "ENTRADA", "quantity": 5})

    # Product 2: Exact stock (current == min)
    res_p2 = client.post("/v1/products/", json={
        "name": "Producto Stock Exacto", "sku": "LOW2", "category_id": category_id,
        "cost_price": 10, "sale_price": 20, "min_stock": 10, "max_stock": 100,
        "unit_of_measure": "u", 
    })
    p2_id = res_p2.json()["id"]
    # Set stock to 10 using a stock movement
    client.post("/v1/stock-movements/", json={"product_id": p2_id, "movement_type": "ENTRADA", "quantity": 10})

    # Product 3: Sufficient stock (current > min)
    res_p3 = client.post("/v1/products/", json={
        "name": "Producto Stock Suficiente", "sku": "OK1", "category_id": category_id,
        "cost_price": 10, "sale_price": 20, "min_stock": 10, "max_stock": 100,
        "unit_of_measure": "u", 
    })
    p3_id = res_p3.json()["id"]
    # Set stock to 11 using a stock movement
    client.post("/v1/stock-movements/", json={"product_id": p3_id, "movement_type": "ENTRADA", "quantity": 11})

    # Act
    response = client.get("/v1/reports/low-stock")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    # Should only return the two products with low or exact stock
    assert len(data) == 2
    skus_in_response = {p["sku"] for p in data}
    assert "LOW1" in skus_in_response
    assert "LOW2" in skus_in_response
    assert "OK1" not in skus_in_response


def test_get_stock_valuation(
    override_product_use_cases,
    override_category_use_cases,
    override_stock_movement_use_cases,
    db_session: Session,
):
    """Test the stock valuation report endpoint."""
    # Arrange: Create a category and two products with different stock and cost
    res_cat = client.post("/v1/categories/", json={"name": "Valuation Category"})
    category_id = res_cat.json()["id"]

    # Product 1: 10 units * $5.50/unit = $55.00
    res_p1 = client.post("/v1/products/", json={
        "name": "Producto Val 1", "sku": "PV1", "category_id": category_id,
        "cost_price": 5.50, "sale_price": 10, "min_stock": 1, "max_stock": 100,
        "unit_of_measure": "u"
    })
    client.post("/v1/stock-movements/", json={"product_id": res_p1.json()["id"], "movement_type": "ENTRADA", "quantity": 10})

    # Product 2: 20 units * $2.00/unit = $40.00
    res_p2 = client.post("/v1/products/", json={
        "name": "Producto Val 2", "sku": "PV2", "category_id": category_id,
        "cost_price": 2.00, "sale_price": 5, "min_stock": 1, "max_stock": 100,
        "unit_of_measure": "u"
    })
    client.post("/v1/stock-movements/", json={"product_id": res_p2.json()["id"], "movement_type": "ENTRADA", "quantity": 20})

    # Expected total valuation: 55.00 + 40.00 = 95.00

    # Act
    response = client.get("/v1/reports/stock-valuation")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["total_valuation"] == 95.0
    assert len(data["products"]) == 2
    assert data["products"][0]["valuation"] == 55.0
    assert data["products"][1]["valuation"] == 40.0


def test_get_sales_summary_report(
    override_product_use_cases,
    override_category_use_cases,
    override_stock_movement_use_cases,
    db_session: Session,
):
    """Test the sales summary report endpoint."""
    # Arrange: Create a category and two products
    res_cat = client.post("/v1/categories/", json={"name": "Sales Category"})
    category_id = res_cat.json()["id"]

    # Product 1: Sells 5 units at $20 each
    res_p1 = client.post("/v1/products/", json={
        "name": "Producto Venta 1", "sku": "SALE1", "category_id": category_id,
        "cost_price": 10, "sale_price": 20, "min_stock": 1, "max_stock": 100,
        "unit_of_measure": "u"
    })
    p1_id = res_p1.json()["id"]
    client.post("/v1/stock-movements/", json={"product_id": p1_id, "movement_type": "ENTRADA", "quantity": 50})
    client.post("/v1/stock-movements/", json={"product_id": p1_id, "movement_type": "SALIDA", "quantity": 5})

    # Product 2: Sells 2 units at $15 each
    res_p2 = client.post("/v1/products/", json={
        "name": "Producto Venta 2", "sku": "SALE2", "category_id": category_id,
        "cost_price": 5, "sale_price": 15, "min_stock": 1, "max_stock": 100,
        "unit_of_measure": "u"
    })
    p2_id = res_p2.json()["id"]
    client.post("/v1/stock-movements/", json={"product_id": p2_id, "movement_type": "ENTRADA", "quantity": 50})
    client.post("/v1/stock-movements/", json={"product_id": p2_id, "movement_type": "SALIDA", "quantity": 2})

    # Expected revenue: (5 * 20) + (2 * 15) = 130
    # Expected COGS: (5 * 10) + (2 * 5) = 60
    # Expected Profit: 130 - 60 = 70

    # Act
    response = client.get("/v1/reports/sales-summary")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["total_revenue"] == 130.0
    assert data["total_units_sold"] == 7
    assert data["total_cost_of_goods_sold"] == 60.0
    assert data["total_profit"] == 70.0
    assert len(data["products_sold"]) == 2


def test_get_sales_summary_ignores_movements_of_deleted_products(
    override_product_use_cases,
    override_category_use_cases,
    override_stock_movement_use_cases,
    db_session: Session,
):
    """
    Test that the sales summary report gracefully handles movements
    for products that have been deleted.
    """
    # Arrange: Create a category and a product
    res_cat = client.post("/v1/categories/", json={"name": "Deleted Product Category"})
    category_id = res_cat.json()["id"]

    res_p1 = client.post("/v1/products/", json={
        "name": "Producto a Borrar", "sku": "DEL1", "category_id": category_id,
        "cost_price": 10, "sale_price": 20, "min_stock": 1, "max_stock": 100,
        "unit_of_measure": "u"
    })
    p1_id = res_p1.json()["id"]

    # Create an entry and a sale for this product
    client.post("/v1/stock-movements/", json={"product_id": p1_id, "movement_type": "ENTRADA", "quantity": 10})
    client.post("/v1/stock-movements/", json={"product_id": p1_id, "movement_type": "SALIDA", "quantity": 5})

    # Now, delete the product
    delete_res = client.delete(f"/v1/products/{p1_id}")
    assert delete_res.status_code == 204

    # Act: Get the sales summary report
    response = client.get("/v1/reports/sales-summary")

    # Assert: The report should be empty as the only product with sales was deleted
    assert response.status_code == 200
    data = response.json()
    assert data["total_revenue"] == 0.0
    assert data["total_units_sold"] == 0
    assert len(data["products_sold"]) == 0