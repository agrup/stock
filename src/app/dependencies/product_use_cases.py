from fastapi import Depends
from sqlalchemy.orm import Session

from src.infrastructure.sqlalchemy.session import get_session
from src.repositories.sqlalchemy_category_repository import SqlAlchemyCategoryRepository
from src.repositories.sqlalchemy_supplier_repository import (
    SqlAlchemySupplierRepository,
)
from src.repositories.sqlalchemy_product_repository import SqlAlchemyProductRepository
from src.use_cases.create_product import CreateProductUseCase
from src.use_cases.get_all_products import GetAllProductsUseCase
from src.use_cases.get_product_by_id import GetProductByIdUseCase
from src.use_cases.update_product import UpdateProductUseCase
from src.use_cases.get_stock_valuation import GetStockValuationUseCase
from src.use_cases.get_low_stock_products import GetLowStockProductsUseCase
from src.use_cases.delete_product import DeleteProductUseCase


class ProductUseCasesContainer:
    def __init__(self, session: Session = Depends(get_session)):
        self._session = session

    def create_product(self) -> CreateProductUseCase:
        return CreateProductUseCase(
            product_repo=SqlAlchemyProductRepository(self._session),
            category_repo=SqlAlchemyCategoryRepository(self._session),
            supplier_repo=SqlAlchemySupplierRepository(self._session),
        )

    def get_all_products(self) -> GetAllProductsUseCase:
        return GetAllProductsUseCase(SqlAlchemyProductRepository(self._session))

    def get_product_by_id(self) -> GetProductByIdUseCase:
        return GetProductByIdUseCase(SqlAlchemyProductRepository(self._session))

    def update_product(self) -> UpdateProductUseCase:
        return UpdateProductUseCase(
            product_repo=SqlAlchemyProductRepository(self._session),
            category_repo=SqlAlchemyCategoryRepository(self._session),
            supplier_repo=SqlAlchemySupplierRepository(self._session),
        )

    def delete_product(self) -> DeleteProductUseCase:
        return DeleteProductUseCase(SqlAlchemyProductRepository(self._session))

    def get_low_stock_products(self) -> GetLowStockProductsUseCase:
        return GetLowStockProductsUseCase(SqlAlchemyProductRepository(self._session))

    def get_stock_valuation(self) -> GetStockValuationUseCase:
        return GetStockValuationUseCase(SqlAlchemyProductRepository(self._session))


product_container = ProductUseCasesContainer()
