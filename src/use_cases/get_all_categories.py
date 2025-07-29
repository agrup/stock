from typing import List

from src.app.dependencies.common_filters import PaginationParams
from src.domain.category import Category
from src.interfaces.category_repository import CategoryRepository


class GetAllCategoriesUseCase:
    def __init__(self, category_repo: CategoryRepository):
        self.category_repo = category_repo

    def execute(self, commons: PaginationParams) -> List[Category]:
        return self.category_repo.get_all(skip=commons.skip, limit=commons.limit)
