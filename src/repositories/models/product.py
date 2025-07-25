from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infrastructure.sqlalchemy.base import Base
from src.repositories.models.category import CategoryModel


class ProductModel(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), index=True)
    sku: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    description: Mapped[str | None] = mapped_column(String(255), nullable=True)
    unit_of_measure: Mapped[str] = mapped_column(String(20))
    cost_price: Mapped[float] = mapped_column(Float)
    sale_price: Mapped[float] = mapped_column(Float)
    min_stock: Mapped[int] = mapped_column(Integer)
    max_stock: Mapped[int] = mapped_column(Integer)
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"))

    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=func.now(), onupdate=func.now()
    )

    category: Mapped["CategoryModel"] = relationship(back_populates="products")
