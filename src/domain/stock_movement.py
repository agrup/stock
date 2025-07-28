from __future__ import annotations
from datetime import datetime
from pydantic import BaseModel, ConfigDict

from src.domain.product import Product
from src.repositories.models.stock_movement import MovementType


class StockMovement(BaseModel):
    id: int | None = None
    product_id: int
    movement_type: MovementType
    quantity: int
    reason: str | None = None
    created_at: datetime | None = None

    product: Product | None = None

    model_config = ConfigDict(from_attributes=True)