from src.core.suppliers.exceptions import SupplierNotFound
from src.interfaces.supplier_repository import SupplierRepository


class DeleteSupplierUseCase:
    def __init__(self, repository: SupplierRepository):
        self.repository = repository

    def execute(self, supplier_id: int) -> None:
        if not self.repository.get_by_id(supplier_id):
            raise SupplierNotFound()

        self.repository.delete(supplier_id)