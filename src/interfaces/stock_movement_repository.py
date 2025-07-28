from typing import List, Optional, Protocol

from src.domain.stock_movement import StockMovement


class StockMovementRepository(Protocol):
    def create(self, movement: StockMovement) -> StockMovement:
        ...

    def get_all(
        self, product_id: Optional[int] = None
    ) -> List[StockMovement]: ...

    def get_by_id(self, movement_id: int) -> Optional[StockMovement]:
        ...

    def delete(self, movement_id: int) -> None:
        ...
