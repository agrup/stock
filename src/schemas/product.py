from pydantic import BaseModel, ConfigDict, Field


class CreateProductSchema(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    sku: str = Field(..., min_length=2, max_length=50)
    description: str | None = Field(None, max_length=255)
    unit_of_measure: str = Field(..., max_length=20)
    cost_price: float = Field(..., gt=0)
    sale_price: float = Field(..., gt=0)
    min_stock: int = Field(..., ge=0)
    max_stock: int = Field(..., ge=0)
    category_id: int


class ProductResponseSchema(BaseModel):
    id: int
    name: str
    sku: str
    description: str | None
    sale_price: float

    model_config = ConfigDict(from_attributes=True)