from typing import List, Optional, Protocol, Mapping, Any

from src.domain.supplier import Supplier


class SupplierRepository(Protocol):
    """Interfaz para el repositorio de proveedores."""

    def create(self, supplier: Supplier) -> Supplier:
        ...

    def get_by_id(self, supplier_id: int) -> Optional[Supplier]:
        ...

    def get_by_name(self, name: str) -> Optional[Supplier]:
        ...

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Supplier]:
        ...

    def update(self, supplier_id: int, data: Mapping[str, Any]) -> Supplier:
        ...

    def delete(self, supplier_id: int) -> None:
        ...