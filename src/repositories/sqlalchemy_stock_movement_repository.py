from typing import List, Optional
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import select

from src.core.stock_movements.exceptions import StockMovementNotFound
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

    def get_all(
        self, product_id: Optional[int] = None
    ) -> List[StockMovement]:
        query = select(StockMovementModel).order_by(StockMovementModel.id.desc())

        if product_id:
            query = query.where(StockMovementModel.product_id == product_id)

        results = self.session.execute(query).scalars().all()
        return [StockMovement.model_validate(res) for res in results]

    def get_by_id(self, movement_id: int) -> Optional[StockMovement]:
        model = (
            self.session.query(StockMovementModel)
            .options(joinedload(StockMovementModel.product))
            .filter_by(id=movement_id)
            .first()
        )
        return StockMovement.model_validate(model) if model else None

    def delete(self, movement_id: int) -> None:
        model = self.session.query(StockMovementModel).filter_by(id=movement_id).first()
        if not model:
            raise StockMovementNotFound()
        self.session.delete(model)
        self.session.flush()
