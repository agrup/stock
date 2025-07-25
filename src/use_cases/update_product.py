from src.core.product.exceptions import ProductNotFound, CategoryNotFound, ProductAlreadyExists
from src.domain.product import Product
from src.interfaces.product_repository import ProductRepository
from src.interfaces.category_repository import CategoryRepository


class UpdateProductUseCase:
    def __init__(self, product_repo: ProductRepository, category_repo: CategoryRepository):
        self.product_repo = product_repo
        self.category_repo = category_repo

    def execute(self, product_id: int, update_data: dict) -> Product:
        # 1. Verificar que el producto a actualizar exista
        product_to_update = self.product_repo.get_by_id(product_id)
        if not product_to_update:
            raise ProductNotFound()

        # 2. Si se actualiza la categoría, verificar que la nueva categoría exista
        if update_data.get("category_id") and not self.category_repo.get_by_id(update_data["category_id"]):
            raise CategoryNotFound()

        # 3. Si se actualiza el SKU, verificar que no entre en conflicto con otro producto
        new_sku = update_data.get("sku")
        if new_sku and new_sku != product_to_update.sku:
            if self.product_repo.get_by_sku(new_sku):
                raise ProductAlreadyExists()

        return self.product_repo.update(product_id, update_data)