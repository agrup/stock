from fastapi import Depends
from sqlalchemy.orm import Session

from src.infrastructure.sqlalchemy.session import get_session
from src.repositories.sqlalchemy_supplier_repository import (
    SqlAlchemySupplierRepository,  # Ruta corregida
)
from src.use_cases.create_supplier import CreateSupplierUseCase
from src.use_cases.delete_supplier import DeleteSupplierUseCase
from src.use_cases.get_all_suppliers import GetAllSuppliersUseCase
from src.use_cases.get_supplier_by_id import GetSupplierByIdUseCase
from src.use_cases.update_supplier import UpdateSupplierUseCase


class SupplierUseCasesContainer:
    """Contenedor de inyección de dependencias para los casos de uso de proveedores."""

    def __init__(self, session: Session = Depends(get_session)):
        self._session = session

    def create_supplier(self) -> CreateSupplierUseCase:
        return CreateSupplierUseCase(SqlAlchemySupplierRepository(self._session))

    def get_all_suppliers(self) -> GetAllSuppliersUseCase:
        return GetAllSuppliersUseCase(SqlAlchemySupplierRepository(self._session))

    def get_supplier_by_id(self) -> GetSupplierByIdUseCase:
        return GetSupplierByIdUseCase(SqlAlchemySupplierRepository(self._session))

    def update_supplier(self) -> UpdateSupplierUseCase:
        return UpdateSupplierUseCase(SqlAlchemySupplierRepository(self._session))

    def delete_supplier(self) -> DeleteSupplierUseCase:
        return DeleteSupplierUseCase(SqlAlchemySupplierRepository(self._session))


supplier_container = SupplierUseCasesContainer()