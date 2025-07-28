from __future__ import annotations
from pydantic import BaseModel, ConfigDict
from typing import List

# Importamos Product al final para evitar importaciones circulares


class Supplier(BaseModel):
    """Entidad de dominio para un Proveedor."""

    id: int | None = None
    name: str
    contact_person: str | None = None
    email: str | None = None
    phone: str | None = None

    model_config = ConfigDict(from_attributes=True)