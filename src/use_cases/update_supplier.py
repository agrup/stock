from src.core.suppliers.exceptions import SupplierAlreadyExists, SupplierNotFound
from src.domain.supplier import Supplier
from src.interfaces.supplier_repository import SupplierRepository


class UpdateSupplierUseCase:
    def __init__(self, repository: SupplierRepository):
        self.repository = repository

    def execute(self, supplier_id: int, data: dict) -> Supplier:
        if not self.repository.get_by_id(supplier_id):
            raise SupplierNotFound()

        if "name" in data:
            existing = self.repository.get_by_name(data["name"])
            if existing and existing.id != supplier_id:
                raise SupplierAlreadyExists()

        return self.repository.update(supplier_id, data)