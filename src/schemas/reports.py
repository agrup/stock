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


class ProductSalesSummarySchema(BaseModel):
    """Schema for a single product's sales summary."""
    product_id: int
    product_name: str
    sku: str
    units_sold: int
    revenue: float
    cost_of_goods_sold: float
    profit: float

class SalesSummaryResponseSchema(BaseModel):
    """Schema for the overall sales summary report."""
    total_revenue: float
    total_units_sold: int
    total_cost_of_goods_sold: float
    total_profit: float
    products_sold: List[ProductSalesSummarySchema]