from src.interfaces.product_repository import ProductRepository


class GetStockValuationUseCase:
    def __init__(self, product_repo: ProductRepository):
        self.product_repo = product_repo

    def execute(self) -> dict:
        """Executes the stock valuation logic."""
        return self.product_repo.get_stock_valuation()