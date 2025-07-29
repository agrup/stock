from src.core.category.exceptions import CategoryAlreadyExists, CategoryNotFound
from src.domain.category import Category
from src.interfaces.category_repository import CategoryRepository
from typing import Mapping, Any


class UpdateCategoryUseCase:
    def __init__(self, category_repo: CategoryRepository):
        self.category_repo = category_repo

    def execute(self, category_id: int, update_data: Mapping[str, Any]) -> Category:
        if not self.category_repo.get_by_id(category_id):
            raise CategoryNotFound()

        new_name = update_data.get("name")
        if new_name:
            existing_category = self.category_repo.get_by_name(new_name)
            if existing_category and existing_category.id != category_id:
                raise CategoryAlreadyExists()

        return self.category_repo.update(category_id, update_data)
