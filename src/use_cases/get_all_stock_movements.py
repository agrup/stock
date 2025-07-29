from datetime import date
from typing import List, Optional

from src.domain.stock_movement import StockMovement
from src.interfaces.stock_movement_repository import StockMovementRepository
from src.app.dependencies.common_filters import CommonFilterParams


class GetAllStockMovementsUseCase:
    def __init__(self, movement_repo: StockMovementRepository):
        self.movement_repo = movement_repo

    def execute(
        self,
        commons: CommonFilterParams,
        product_id: Optional[int] = None
    ) -> List[StockMovement]:
        return self.movement_repo.get_all(
            product_id=product_id, skip=commons.skip, limit=commons.limit,
            start_date=commons.start_date, end_date=commons.end_date
        )
