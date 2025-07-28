from __future__ import annotations

from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infrastructure.sqlalchemy.base import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.repositories.models.product import ProductModel


class SupplierModel(Base):
    """Modelo de datos para los Proveedores."""

    __tablename__ = "suppliers"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(index=True, unique=True)
    contact_person: Mapped[str | None]
    email: Mapped[str | None]
    phone: Mapped[str | None]

    products: Mapped[list["ProductModel"]] = relationship(back_populates="supplier")

    def __repr__(self) -> str:
        return (
            f"<SupplierModel(id={self.id}, name='{self.name}', email='{self.email}')>"
        )