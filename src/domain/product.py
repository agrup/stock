from __future__ import annotations
from pydantic import BaseModel, ConfigDict, Field
from typing import Optional


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

    # Relationships are now nested objects
    category: "Category"
    supplier: Optional["Supplier"] = None

    model_config = ConfigDict(from_attributes=True)


# Late imports to resolve circular dependency
from src.domain.category import Category  # noqa: E402
from src.domain.supplier import Supplier  # noqa: E402

Product.model_rebuild()
