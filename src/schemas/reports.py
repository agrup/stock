from pydantic import BaseModel
from typing import List


class ProductValuationSchema(BaseModel):
    """Schema for a single product's valuation."""
    product_id: int
    product_name: str
    sku: str
    current_stock: int
    cost_price: float
    valuation: float


class StockValuationResponseSchema(BaseModel):
    """Schema for the overall stock valuation report."""
    total_valuation: float
    products: List[ProductValuationSchema]