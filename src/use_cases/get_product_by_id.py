from src.core.product.exceptions import ProductNotFound
from src.domain.product import Product
from src.interfaces.product_repository import ProductRepository


class GetProductByIdUseCase:
    def __init__(self, product_repo: ProductRepository):
        self.product_repo = product_repo

    def execute(self, product_id: int) -> Product:
        product = self.product_repo.get_by_id(product_id)
        if not product:
            raise ProductNotFound()
        return product
