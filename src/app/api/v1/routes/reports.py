from typing import Annotated, List
from fastapi import APIRouter, Depends

from src.app.dependencies.product_use_cases import product_container
from src.schemas.product import ProductResponseSchema
from src.schemas.reports import StockValuationResponseSchema
from src.use_cases.get_low_stock_products import GetLowStockProductsUseCase
from src.use_cases.get_stock_valuation import GetStockValuationUseCase

router = APIRouter(prefix="/reports", tags=["Reports"])


@router.get(
    "/low-stock",
    response_model=List[ProductResponseSchema],
    summary="Get Low Stock Products",
    description="Retrieves a list of products where the current stock is less than or equal to the minimum stock level.",
)
def get_low_stock_products(
    use_case: Annotated[
        GetLowStockProductsUseCase,
        Depends(product_container.get_low_stock_products),
    ],
):
    low_stock_products = use_case.execute()
    return low_stock_products


@router.get(
    "/stock-valuation",
    response_model=StockValuationResponseSchema,
    summary="Get Stock Valuation",
    description="Calculates the total valuation of the current stock based on the cost price of each product.",
)
def get_stock_valuation(
    use_case: Annotated[
        GetStockValuationUseCase, Depends(product_container.get_stock_valuation)
    ],
):
    valuation_data = use_case.execute()
    return valuation_data
