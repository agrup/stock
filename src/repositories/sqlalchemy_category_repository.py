from typing import List, Optional

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

    def get_by_name(self, name: str) -> Optional[Category]:
        category_model = self.session.query(CategoryModel).filter_by(name=name).first()
        if not category_model:
            return None
        return Category.model_validate(category_model)

    def create(self, category: Category) -> Category:
        category_model = CategoryModel(**category.model_dump(exclude={"id"}))
        self.session.add(category_model)
        self.session.commit()
        self.session.refresh(category_model)
        return Category.model_validate(category_model)

    def get_all(self) -> List[Category]:
        category_models = self.session.query(CategoryModel).all()
        return [
            Category.model_validate(category) for category in category_models
        ]