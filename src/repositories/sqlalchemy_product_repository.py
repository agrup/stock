from typing import Optional

from sqlalchemy.orm import Session

from src.domain.product import Product
from src.interfaces.product_repository import ProductRepository
from src.repositories.models.product import ProductModel


class SqlAlchemyProductRepository(ProductRepository):
    def __init__(self, session: Session):
        self.session = session

    def create(self, product: Product) -> Product:
        product_model = ProductModel(**product.model_dump())
        self.session.add(product_model)
        self.session.commit()
        self.session.refresh(product_model)
        return Product.model_validate(product_model)

    def get_by_sku(self, sku: str) -> Optional[Product]:
        product_model = (
            self.session.query(ProductModel).filter_by(sku=sku).first()
        )
        if not product_model:
            return None
        return Product.model_validate(product_model)