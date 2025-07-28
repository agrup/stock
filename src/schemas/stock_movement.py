from pydantic import BaseModel, ConfigDict, Field

from src.repositories.models.stock_movement import MovementType


class CreateStockMovementSchema(BaseModel):
    product_id: int
    movement_type: MovementType
    quantity: int = Field(..., gt=0)
    reason: str | None = Field(None, max_length=255)


class StockMovementResponseSchema(BaseModel):
    id: int
    product_id: int
    movement_type: MovementType
    quantity: int

    model_config = ConfigDict(from_attributes=True)