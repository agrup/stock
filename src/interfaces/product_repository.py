from abc import ABC, abstractmethod
from typing import Optional

from src.domain.product import Product


class ProductRepository(ABC):
    @abstractmethod
    def create(self, product: Product) -> Product:
        raise NotImplementedError

    @abstractmethod
    def get_by_sku(self, sku: str) -> Optional[Product]:
        raise NotImplementedError