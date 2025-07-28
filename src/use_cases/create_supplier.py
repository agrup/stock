from src.core.suppliers.exceptions import SupplierAlreadyExists
from src.domain.supplier import Supplier
from src.interfaces.supplier_repository import SupplierRepository


class CreateSupplierUseCase:
    def __init__(self, repository: SupplierRepository):
        self.repository = repository

    def execute(self, supplier: Supplier) -> Supplier:
        existing_supplier = self.repository.get_by_name(supplier.name)
        if existing_supplier:
            raise SupplierAlreadyExists()

        return self.repository.create(supplier)