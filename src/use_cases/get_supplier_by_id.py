from src.core.suppliers.exceptions import SupplierNotFound
from src.domain.supplier import Supplier
from src.interfaces.supplier_repository import SupplierRepository


class GetSupplierByIdUseCase:
    def __init__(self, repository: SupplierRepository):
        self.repository = repository

    def execute(self, supplier_id: int) -> Supplier:
        supplier = self.repository.get_by_id(supplier_id)
        if not supplier:
            raise SupplierNotFound()
        return supplier