from typing import List
from src.domain.supplier import Supplier
from src.interfaces.supplier_repository import SupplierRepository


class GetAllSuppliersUseCase:
    def __init__(self, repository: SupplierRepository):
        self.repository = repository

    def execute(self) -> List[Supplier]:
        return self.repository.get_all()