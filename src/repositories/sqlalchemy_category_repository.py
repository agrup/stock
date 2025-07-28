from typing import List, Optional

from sqlalchemy.orm import Session, joinedload

from src.core.category.exceptions import CategoryInUseError
from src.domain.category import Category
from src.interfaces.category_repository import CategoryRepository
from src.repositories.models.category import CategoryModel


class SqlAlchemyCategoryRepository(CategoryRepository):
    """Implementación concreta del repositorio de categorías con SQLAlchemy."""

    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, category_id: int) -> Optional[Category]:
        category_model = (
            self.session.query(CategoryModel)
            .options(joinedload(CategoryModel.products))
            .filter_by(id=category_id)
            .first()
        )
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
        self.session.flush()
        return Category.model_validate(category_model)

    def get_all(self) -> List[Category]:
        category_models = (
            self.session.query(CategoryModel)
            .options(joinedload(CategoryModel.products))
            .order_by(CategoryModel.id)
            .all()
        )
        return [Category.model_validate(category) for category in category_models]

    def update(self, category_id: int, category_data: dict) -> Category:
        category_model = (
            self.session.query(CategoryModel).filter_by(id=category_id).one()
        )
        for key, value in category_data.items():
            if value is not None:
                setattr(category_model, key, value)
        self.session.flush()
        return Category.model_validate(category_model)

    def delete(self, category_id: int) -> None:
        # The existence check is done in the use case, but we need to fetch
        # the object with its products to check for usage.
        category_model = self.session.query(CategoryModel).options(
            joinedload(CategoryModel.products)
        ).filter_by(id=category_id).one()

        if category_model.products:
            raise CategoryInUseError()

        self.session.delete(category_model)
        self.session.flush()
