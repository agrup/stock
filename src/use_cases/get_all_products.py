from typing import List

from src.domain.product import Product
from src.interfaces.product_repository import ProductRepository


class GetAllProductsUseCase:
    def __init__(self, product_repo: ProductRepository):
        self.product_repo = product_repo

    def execute(self) -> List[Product]:
        return self.product_repo.get_all()