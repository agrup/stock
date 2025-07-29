from typing import List
from src.domain.supplier import Supplier
from src.interfaces.supplier_repository import SupplierRepository
from src.app.dependencies.common_filters import PaginationParams


class GetAllSuppliersUseCase:
    def __init__(self, repository: SupplierRepository):
        self.repository = repository

    def execute(self, commons: PaginationParams) -> List[Supplier]:
        return self.repository.get_all(skip=commons.skip, limit=commons.limit)