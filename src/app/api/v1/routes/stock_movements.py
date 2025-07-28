from typing import Annotated, List, Optional
from fastapi import APIRouter, Depends, HTTPException, status

from src.app.dependencies.stock_movement_use_cases import stock_movement_container
from src.core.product.exceptions import ProductNotFound
from src.core.stock_movements.exceptions import InsufficientStockError, StockMovementNotFound
from src.schemas.stock_movement import (
    CreateStockMovementSchema,
    StockMovementResponseSchema,
)
from src.use_cases.create_stock_movement import CreateStockMovementUseCase
from src.use_cases.delete_stock_movement import DeleteStockMovementUseCase
from src.use_cases.get_all_stock_movements import GetAllStockMovementsUseCase

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


@router.get("/", response_model=List[StockMovementResponseSchema])
def get_all_stock_movements(
    use_case: Annotated[
        GetAllStockMovementsUseCase,
        Depends(stock_movement_container.get_all_stock_movements),
    ],
    product_id: Optional[int] = None,
):
    movements = use_case.execute(product_id=product_id)
    return movements


@router.delete("/{movement_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_stock_movement(
    movement_id: int,
    use_case: Annotated[
        DeleteStockMovementUseCase,
        Depends(stock_movement_container.delete_stock_movement),
    ],
):
    try:
        use_case.execute(movement_id)
    except (StockMovementNotFound, ProductNotFound) as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
