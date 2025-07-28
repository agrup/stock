from typing import List, Optional

from src.domain.stock_movement import StockMovement
from src.interfaces.stock_movement_repository import StockMovementRepository


class GetAllStockMovementsUseCase:
    def __init__(self, movement_repo: StockMovementRepository):
        self.movement_repo = movement_repo

    def execute(
        self, product_id: Optional[int] = None
    ) -> List[StockMovement]:
        return self.movement_repo.get_all(product_id=product_id)
