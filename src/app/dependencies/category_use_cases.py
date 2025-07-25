from fastapi import Depends
from sqlalchemy.orm import Session

from src.infrastructure.sqlalchemy.session import get_session
from src.repositories.sqlalchemy_category_repository import SqlAlchemyCategoryRepository
from src.use_cases.create_category import CreateCategoryUseCase
from src.use_cases.get_all_categories import GetAllCategoriesUseCase


class CategoryUseCasesContainer:
    def __init__(self, session: Session = Depends(get_session)):
        self._session = session

    def create_category(self) -> CreateCategoryUseCase:
        return CreateCategoryUseCase(SqlAlchemyCategoryRepository(self._session))

    def get_all_categories(self) -> GetAllCategoriesUseCase:
        return GetAllCategoriesUseCase(SqlAlchemyCategoryRepository(self._session))


category_container = CategoryUseCasesContainer()