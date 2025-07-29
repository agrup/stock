from typing import List, Optional, Mapping, Any

from sqlalchemy.orm import Session, joinedload
from src.core.product.exceptions import ProductNotFound

from src.domain.product import Product
from src.interfaces.product_repository import ProductRepository
from src.repositories.models.product import ProductModel


class SqlAlchemyProductRepository(ProductRepository):
    """Implementación concreta del repositorio de productos con SQLAlchemy."""

    def __init__(self, session: Session):
        self.session = session

    def create(self, product: Product) -> Product:
        # Exclude nested objects and prepare data for the DB model
        product_data = product.model_dump(exclude={"id", "category", "supplier"})
        product_data["category_id"] = product.category.id
        if product.supplier:
            product_data["supplier_id"] = product.supplier.id

        product_model = ProductModel(**product_data)
        self.session.add(product_model)
        self.session.flush()
        return Product.model_validate(product_model)

    def get_by_sku(self, sku: str) -> Optional[Product]:
        product_model = self.session.query(ProductModel).filter_by(sku=sku).first()
        if not product_model:
            return None
        return Product.model_validate(product_model)

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Product]:
        product_models = (
            self.session.query(ProductModel)
            .options(
                joinedload(ProductModel.category), joinedload(ProductModel.supplier)
            )
            .offset(skip)
            .limit(limit)
            .all()
        )
        return [Product.model_validate(product) for product in product_models]

    def get_by_id(self, product_id: int) -> Optional[Product]:
        product_model = (
            self.session.query(ProductModel)
            .options(
                joinedload(ProductModel.category), joinedload(ProductModel.supplier)
            )
            .filter_by(id=product_id).first()
        )
        if not product_model:
            return None
        return Product.model_validate(product_model)

    def update(self, product_id: int, product_data: Mapping[str, Any]) -> Product:
        product_model = self.session.query(ProductModel).filter_by(id=product_id).first()
        if not product_model:
            raise ProductNotFound()

        for key, value in product_data.items():
            if value is not None:
                setattr(product_model, key, value)

        self.session.flush()
        return Product.model_validate(product_model)

    def delete(self, product_id: int) -> None:
        product_model = self.session.query(ProductModel).filter_by(id=product_id).first()
        if not product_model:
            raise ProductNotFound()
        self.session.delete(product_model)
        self.session.flush()

    def get_low_stock(self) -> List[Product]:
        product_models = (
            self.session.query(ProductModel)
            .options(
                joinedload(ProductModel.category), joinedload(ProductModel.supplier)
            )
            .filter(ProductModel.current_stock <= ProductModel.min_stock)
            .all()
        )
        return [Product.model_validate(product) for product in product_models]

    def get_stock_valuation(self) -> dict:
        products = self.get_all()
        total_valuation = 0.0
        product_valuations = []

        for product in products:
            valuation = product.current_stock * product.cost_price
            total_valuation += valuation
            product_valuations.append({
                "product_id": product.id,
                "product_name": product.name,
                "sku": product.sku,
                "current_stock": product.current_stock,
                "cost_price": product.cost_price,
                "valuation": valuation,
            })

        return {"total_valuation": total_valuation, "products": product_valuations}
