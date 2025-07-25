from typing import Optional, Protocol

from src.domain.category import Category


class CategoryRepository(Protocol):
    def get_by_id(self, category_id: int) -> Optional[Category]:
        """Busca una categoría por su ID."""
        ...