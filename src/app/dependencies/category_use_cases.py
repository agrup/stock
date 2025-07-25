from fastapi import Depends
from sqlalchemy.orm import Session

from src.infrastructure.sqlalchemy.session import get_session
from src.repositories.sqlalchemy_category_repository import SqlAlchemyCategoryRepository
from src.use_cases.create_category import CreateCategoryUseCase
from src.use_cases.get_all_categories import GetAllCategoriesUseCase
from src.use_cases.get_category_by_id import GetCategoryByIdUseCase
from src.use_cases.update_category import UpdateCategoryUseCase
from src.use_cases.delete_category import DeleteCategoryUseCase


class CategoryUseCasesContainer:
    def __init__(self, session: Session = Depends(get_session)):
        self._session = session

    def create_category(self) -> CreateCategoryUseCase:
        return CreateCategoryUseCase(SqlAlchemyCategoryRepository(self._session))

    def get_all_categories(self) -> GetAllCategoriesUseCase:
        return GetAllCategoriesUseCase(SqlAlchemyCategoryRepository(self._session))

    def get_category_by_id(self) -> GetCategoryByIdUseCase:
        return GetCategoryByIdUseCase(SqlAlchemyCategoryRepository(self._session))

    def update_category(self) -> UpdateCategoryUseCase:
        return UpdateCategoryUseCase(SqlAlchemyCategoryRepository(self._session))

    def delete_category(self) -> DeleteCategoryUseCase:
        return DeleteCategoryUseCase(SqlAlchemyCategoryRepository(self._session))


category_container = CategoryUseCasesContainer()
