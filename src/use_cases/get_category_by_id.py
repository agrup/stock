from src.core.category.exceptions import CategoryNotFound
from src.domain.category import Category
from src.interfaces.category_repository import CategoryRepository


class GetCategoryByIdUseCase:
    def __init__(self, category_repo: CategoryRepository):
        self.category_repo = category_repo

    def execute(self, category_id: int) -> Category:
        category = self.category_repo.get_by_id(category_id)
        if not category:
            raise CategoryNotFound()
        return category
