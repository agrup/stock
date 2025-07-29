from src.core.product.exceptions import (
    ProductAlreadyExists,
    ProductNotFound,
    CategoryForProductNotFound,
    SupplierForProductNotFound,
)
from src.domain.product import Product
from src.interfaces.product_repository import ProductRepository
from src.interfaces.category_repository import CategoryRepository
from src.interfaces.supplier_repository import SupplierRepository
from typing import Mapping, Any

class UpdateProductUseCase:
    def __init__(
        self,
        product_repo: ProductRepository,
        category_repo: CategoryRepository,
        supplier_repo: SupplierRepository,
    ):
        self.product_repo = product_repo
        self.category_repo = category_repo
        self.supplier_repo = supplier_repo

    def execute(self, product_id: int, update_data: Mapping[str, Any]) -> "Product":
        # 1. Verificar que el producto a actualizar exista
        product_to_update = self.product_repo.get_by_id(product_id)
        if not product_to_update:
            raise ProductNotFound()

        # 2. Si se actualiza la categoría, verificar que exista
        if "category_id" in update_data:
            new_category_id = update_data["category_id"]
            # La categoría es obligatoria, no puede ser nula.
            if not new_category_id or not self.category_repo.get_by_id(new_category_id):
                raise CategoryForProductNotFound()

        # 3. Si se actualiza el proveedor, verificar que exista
        if "supplier_id" in update_data:
            new_supplier_id = update_data.get("supplier_id")
            if new_supplier_id and not self.supplier_repo.get_by_id(new_supplier_id):
                raise SupplierForProductNotFound()

        # 4. Si se actualiza el SKU, verificar
        # que no entre en conflicto con otro producto
        new_sku = update_data.get("sku")
        if new_sku and new_sku != product_to_update.sku:
            if self.product_repo.get_by_sku(new_sku):
                raise ProductAlreadyExists()

        return self.product_repo.update(product_id, update_data)
