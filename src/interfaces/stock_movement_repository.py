from typing import Protocol

from src.domain.stock_movement import StockMovement


class StockMovementRepository(Protocol):
    def create(self, movement: StockMovement) -> StockMovement:
        ...