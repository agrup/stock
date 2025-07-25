from src.core.category.exceptions import CategoryInUseError, CategoryNotFound
from src.interfaces.category_repository import CategoryRepository


class DeleteCategoryUseCase:
    def __init__(self, category_repo: CategoryRepository):
        self.category_repo = category_repo

    def execute(self, category_id: int) -> None:
        category_to_delete = self.category_repo.get_by_id(category_id)
        if not category_to_delete:
            raise CategoryNotFound()

        if category_to_delete.products:
            raise CategoryInUseError()

        self.category_repo.delete(category_id)
