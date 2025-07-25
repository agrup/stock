from typing import List, Optional, Protocol

from src.domain.product import Product


class ProductRepository(Protocol):
    def create(self, product: Product) -> Product:
        ...

    def get_by_sku(self, sku: str) -> Optional[Product]:
        ...

    def get_all(self) -> List[Product]:
        ...