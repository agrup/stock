from datetime import date, timedelta
from typing import List, Optional
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func, select

from src.core.stock_movements.exceptions import StockMovementNotFound
from src.domain.stock_movement import StockMovement
from src.interfaces.stock_movement_repository import StockMovementRepository
from src.repositories.models.stock_movement import StockMovementModel
from src.repositories.models.product import ProductModel
from src.repositories.models.stock_movement import MovementType


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
        self,
        product_id: Optional[int] = None,
        skip: int = 0,
        limit: int = 100,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
    ) -> List[StockMovement]:
        query = select(StockMovementModel).options(
            joinedload(StockMovementModel.product)
        ).order_by(StockMovementModel.id.desc())

        if product_id:
            query = query.where(StockMovementModel.product_id == product_id)
        if start_date:
            query = query.where(StockMovementModel.created_at >= start_date)
        if end_date:
            # Add 1 day to end_date to make the filter inclusive of the whole day
            inclusive_end_date = end_date + timedelta(days=1)
            query = query.where(StockMovementModel.created_at < inclusive_end_date)

        query = query.offset(skip).limit(limit)
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
