from src.core.category.exceptions import CategoryNotFound
from src.interfaces.category_repository import CategoryRepository


class DeleteCategoryUseCase:
    def __init__(self, category_repo: CategoryRepository):
        self.category_repo = category_repo

    def execute(self, category_id: int) -> None:
        if not self.category_repo.get_by_id(category_id):
            raise CategoryNotFound()

        self.category_repo.delete(category_id)
