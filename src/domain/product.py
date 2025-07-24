from pydantic import BaseModel, Field


class Product(BaseModel):
    id: int | None = None
    name: str
    sku: str
    description: str | None = None
    unit_of_measure: str
    cost_price: float = Field(gt=0)
    sale_price: float = Field(gt=0)
    min_stock: int = Field(ge=0)
    max_stock: int = Field(ge=0)
    category_id: int