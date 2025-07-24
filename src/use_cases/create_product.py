from src.core.product.exceptions import CategoryNotFound, ProductAlreadyExists
from src.domain.product import Product
from src.interfaces.category_repository import CategoryRepository
from src.interfaces.product_repository import ProductRepository


class CreateProductUseCase:
    def __init__(
        self, product_repo: ProductRepository, category_repo: CategoryRepository
    ):
        self.product_repo = product_repo
        self.category_repo = category_repo

    def execute(self, product_data: Product) -> Product:
        # 1. Verificar que la categoría exista
        category = self.category_repo.get_by_id(product_data.category_id)
        if not category:
            raise CategoryNotFound()

        # 2. Verificar que el SKU no exista
        existing_product = self.product_repo.get_by_sku(product_data.sku)
        if existing_product:
            raise ProductAlreadyExists()

        # 3. Crear el producto
        created_product = self.product_repo.create(product_data)
        return created_product