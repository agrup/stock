from typing import Optional

from sqlalchemy.orm import Session

from src.domain.category import Category
from src.interfaces.category_repository import CategoryRepository
from src.repositories.models.category import CategoryModel


class SqlAlchemyCategoryRepository(CategoryRepository):
    """Implementación concreta del repositorio de categorías con SQLAlchemy."""
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, category_id: int) -> Optional[Category]:
        category_model = self.session.query(CategoryModel).filter_by(id=category_id).first()
        if not category_model:
            return None
        return Category.model_validate(category_model)