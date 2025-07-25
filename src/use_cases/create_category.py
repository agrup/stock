from src.core.category.exceptions import CategoryAlreadyExists
from src.domain.category import Category
from src.interfaces.category_repository import CategoryRepository


class CreateCategoryUseCase:
    def __init__(self, category_repo: CategoryRepository):
        self.category_repo = category_repo

    def execute(self, category_data: Category) -> Category:
        existing_category = self.category_repo.get_by_name(category_data.name)
        if existing_category:
            raise CategoryAlreadyExists()

        return self.category_repo.create(category_data)