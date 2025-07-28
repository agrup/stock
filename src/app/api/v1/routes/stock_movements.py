from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status

from src.app.dependencies.stock_movement_use_cases import stock_movement_container
from src.core.product.exceptions import ProductNotFound
from src.core.stock_movements.exceptions import InsufficientStockError
from src.schemas.stock_movement import (
    CreateStockMovementSchema,
    StockMovementResponseSchema,
)
from src.use_cases.create_stock_movement import CreateStockMovementUseCase

router = APIRouter(prefix="/stock-movements", tags=["Stock Movements"])


@router.post(
    "/",
    response_model=StockMovementResponseSchema,
    status_code=status.HTTP_201_CREATED,
)
def create_stock_movement(
    movement_data: CreateStockMovementSchema,
    use_case: Annotated[
        CreateStockMovementUseCase,
        Depends(stock_movement_container.create_stock_movement),
    ],
):
    try:
        created_movement = use_case.execute(movement_data.model_dump())
        return created_movement
    except (ProductNotFound, InsufficientStockError) as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)