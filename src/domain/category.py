from __future__ import annotations
from pydantic import BaseModel, ConfigDict
from typing import List

# Importamos Product al final para evitar importaciones circulares


class Category(BaseModel):
    id: int | None = None
    name: str
    description: str | None = None
    products: List["Product"] = []

    model_config = ConfigDict(from_attributes=True)


from src.domain.product import Product

Category.model_rebuild()
