from src.interfaces.stock_movement_repository import StockMovementRepository
from src.repositories.models.stock_movement import MovementType
from src.schemas.reports import SalesSummaryResponseSchema, ProductSalesSummarySchema
from collections import defaultdict
from typing import Optional
from datetime import date
from src.app.dependencies.common_filters import CommonFilterParams


class GetSalesSummaryUseCase:
    def __init__(self, movement_repo: StockMovementRepository):
        self.movement_repo = movement_repo

    def execute(self, commons: CommonFilterParams) -> SalesSummaryResponseSchema:
        """
        Retrieves all sales movements and aggregates them into a sales summary.
        Returns a structured response object.
        """
        # We get all movements within the date range and then filter for sales
        # The repository will handle the date filtering.
        # We fetch all movements for the report, so we use a high limit.
        all_movements = self.movement_repo.get_all(
            start_date=commons.start_date, end_date=commons.end_date, limit=10000
        )
        sales_movements = [m for m in all_movements if m.movement_type == MovementType.SALIDA]

        total_revenue = 0.0
        total_units_sold = 0
        total_cost_of_goods_sold = 0.0
        # Use a defaultdict to easily aggregate sales by product
        sales_by_product = defaultdict(lambda: {"units_sold": 0, "revenue": 0, "cost": 0})

        for movement in sales_movements:
            product = movement.product
            # This check is for data integrity, in case a product was deleted
            # but its movements remain.
            if not product:
                continue

            revenue = movement.quantity * product.sale_price
            cost = movement.quantity * product.cost_price
            total_revenue += revenue
            total_units_sold += movement.quantity
            total_cost_of_goods_sold += cost

            sales_by_product[product.id]["units_sold"] += movement.quantity
            sales_by_product[product.id]["revenue"] += revenue
            sales_by_product[product.id]["cost"] += cost
            # Store product info if not already there
            if "product_info" not in sales_by_product[product.id]:
                sales_by_product[product.id]["product_info"] = product

        products_sold = [
            ProductSalesSummarySchema(
                product_id=pid, product_name=data["product_info"].name, sku=data["product_info"].sku,
                units_sold=data["units_sold"], revenue=data["revenue"],
                cost_of_goods_sold=data["cost"], profit=data["revenue"] - data["cost"]
            ) for pid, data in sales_by_product.items()
        ]

        total_profit = total_revenue - total_cost_of_goods_sold

        return SalesSummaryResponseSchema(
            total_revenue=total_revenue, total_units_sold=total_units_sold,
            total_cost_of_goods_sold=total_cost_of_goods_sold, total_profit=total_profit,
            products_sold=products_sold
        )