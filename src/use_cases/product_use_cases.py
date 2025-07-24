from fastapi import Depends
from sqlalchemy.orm import Session

from src.infrastructure.sqlalchemy.session import get_session
from src.repositories.sqlalchemy_category_repository import SqlAlchemyCategoryRepository
from src.repositories.sqlalchemy_product_repository import SqlAlchemyProductRepository
from src.use_cases.create_product import CreateProductUseCase


def get_create_product_use_case(
    session: Session = Depends(get_session),
) -> CreateProductUseCase:
    product_repo = SqlAlchemyProductRepository(session)
    category_repo = SqlAlchemyCategoryRepository(session)
    return CreateProductUseCase(product_repo=product_repo, category_repo=category_repo)