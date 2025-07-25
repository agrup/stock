from typing import List, Optional

from sqlalchemy.orm import Session

from src.domain.product import Product
from src.interfaces.product_repository import ProductRepository
from src.repositories.models.product import ProductModel


class SqlAlchemyProductRepository(ProductRepository):
    """Implementación concreta del repositorio de productos con SQLAlchemy."""
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

    def get_all(self) -> List[Product]:
        product_models = self.session.query(ProductModel).all()
        return [
            Product.model_validate(product) for product in product_models
        ]

    def get_by_id(self, product_id: int) -> Optional[Product]:
        product_model = self.session.query(ProductModel).filter_by(id=product_id).first()
        if not product_model:
            return None
        return Product.model_validate(product_model)

    def update(self, product_id: int, product_data: dict) -> Product:
        product_model = self.session.query(ProductModel).filter_by(id=product_id).one()

        for key, value in product_data.items():
            if value is not None:
                setattr(product_model, key, value)

        self.session.commit()
        self.session.refresh(product_model)
        return Product.model_validate(product_model)