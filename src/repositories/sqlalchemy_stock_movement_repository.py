from sqlalchemy.orm import Session

from src.domain.stock_movement import StockMovement
from src.interfaces.stock_movement_repository import StockMovementRepository
from src.repositories.models.stock_movement import StockMovementModel


class SqlAlchemyStockMovementRepository(StockMovementRepository):
    def __init__(self, session: Session):
        self.session = session

    def create(self, movement: StockMovement) -> StockMovement:
        movement_model = StockMovementModel(
            **movement.model_dump(exclude={"id", "product"})
        )
        self.session.add(movement_model)
        self.session.flush()  # Flush to get the ID, but don't commit.
        return StockMovement.model_validate(movement_model)