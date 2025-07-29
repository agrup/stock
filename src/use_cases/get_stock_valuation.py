from src.interfaces.product_repository import ProductRepository
from src.schemas.reports import StockValuationResponseSchema, ProductValuationSchema


class GetStockValuationUseCase:
    def __init__(self, product_repo: ProductRepository):
        self.product_repo = product_repo

    def execute(self) -> StockValuationResponseSchema:
        """
        Retrieves all products and calculates their stock valuation.
        Returns a structured response object.
        """
        # For valuation, we typically want all products, so we fetch with a high limit.
        products = self.product_repo.get_all(limit=10000)
        total_valuation = 0.0
        product_valuations = []

        for product in products:
            valuation = product.current_stock * product.cost_price
            total_valuation += valuation
            product_valuations.append(ProductValuationSchema(
                product_id=product.id,
                product_name=product.name,
                sku=product.sku,
                current_stock=product.current_stock,
                cost_price=product.cost_price,
                valuation=valuation,
            ))

        return StockValuationResponseSchema(total_valuation=total_valuation, products=product_valuations)