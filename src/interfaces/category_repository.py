from abc import ABC, abstractmethod
from typing import Optional

from src.domain.category import Category


class CategoryRepository(ABC):
    @abstractmethod
    def get_by_id(self, category_id: int) -> Optional[Category]:
        """Busca una categoría por su ID."""
        raise NotImplementedError