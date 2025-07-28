from fastapi import Depends
from sqlalchemy.orm import Session

from src.infrastructure.sqlalchemy.session import get_session
from src.repositories.sqlalchemy_product_repository import SqlAlchemyProductRepository
from src.repositories.sqlalchemy_stock_movement_repository import (
    SqlAlchemyStockMovementRepository,
)
from src.use_cases.create_stock_movement import CreateStockMovementUseCase
from src.use_cases.delete_stock_movement import DeleteStockMovementUseCase
from src.use_cases.get_all_stock_movements import GetAllStockMovementsUseCase


class StockMovementUseCasesContainer:
    def __init__(self, session: Session = Depends(get_session)):
        self._session = session

    def create_stock_movement(self) -> CreateStockMovementUseCase:
        return CreateStockMovementUseCase(
            movement_repo=SqlAlchemyStockMovementRepository(self._session),
            product_repo=SqlAlchemyProductRepository(self._session),
        )

    def get_all_stock_movements(self) -> GetAllStockMovementsUseCase:
        return GetAllStockMovementsUseCase(
            movement_repo=SqlAlchemyStockMovementRepository(self._session)
        )

    def delete_stock_movement(self) -> DeleteStockMovementUseCase:
        return DeleteStockMovementUseCase(
            movement_repo=SqlAlchemyStockMovementRepository(self._session),
            product_repo=SqlAlchemyProductRepository(self._session),
        )


stock_movement_container = StockMovementUseCasesContainer()