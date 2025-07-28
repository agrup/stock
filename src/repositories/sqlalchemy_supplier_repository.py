from typing import List, Optional

from sqlalchemy.orm import Session, joinedload

from src.core.suppliers.exceptions import SupplierInUseError
from src.domain.supplier import Supplier
from src.interfaces.supplier_repository import SupplierRepository
from src.repositories.models.supplier import SupplierModel


class SqlAlchemySupplierRepository(SupplierRepository):
    def __init__(self, session: Session):
        self.session = session

    def create(self, supplier: Supplier) -> Supplier:
        model = SupplierModel(**supplier.model_dump(exclude={"id", "products"}))
        self.session.add(model)
        self.session.flush()
        return Supplier.model_validate(model)

    def get_by_id(self, supplier_id: int) -> Optional[Supplier]:
        model = (
            self.session.query(SupplierModel)
            .options(joinedload(SupplierModel.products))
            .filter_by(id=supplier_id)
            .first()
        )
        return Supplier.model_validate(model) if model else None

    def get_by_name(self, name: str) -> Optional[Supplier]:
        model = self.session.query(SupplierModel).filter_by(name=name).first()
        return Supplier.model_validate(model) if model else None

    def get_all(self) -> List[Supplier]:
        models = (
            self.session.query(SupplierModel)
            .options(joinedload(SupplierModel.products))
            .order_by(SupplierModel.id)
            .all()
        )
        return [Supplier.model_validate(model) for model in models]

    def update(self, supplier_id: int, data: dict) -> Supplier:
        model = self.session.query(SupplierModel).filter_by(id=supplier_id).one()
        for key, value in data.items():
            if value is not None:
                setattr(model, key, value)
        self.session.flush()
        return Supplier.model_validate(model)

    def delete(self, supplier_id: int) -> None:
        model = self.session.query(SupplierModel).options(
            joinedload(SupplierModel.products)
        ).filter_by(id=supplier_id).one()

        if model.products:
            raise SupplierInUseError()

        self.session.delete(model)
        self.session.flush()