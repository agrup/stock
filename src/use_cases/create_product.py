from src.core.product.exceptions import (
    ProductAlreadyExists,
    SupplierForProductNotFound,
    CategoryForProductNotFound,
)
from src.domain.product import Product
from src.interfaces.category_repository import CategoryRepository
from src.interfaces.product_repository import ProductRepository
from src.interfaces.supplier_repository import SupplierRepository


class CreateProductUseCase:
    def __init__(
        self,
        product_repo: ProductRepository,
        category_repo: CategoryRepository,
        supplier_repo: SupplierRepository,
    ):
        self.product_repo = product_repo
        self.category_repo = category_repo
        self.supplier_repo = supplier_repo

    def execute(self, product_data: dict) -> Product:
        # The input is now a dict from the CreateProductSchema

        # 1. Verificar que la categoría exista
        category_id = product_data.get("category_id")
        category = self.category_repo.get_by_id(category_id)
        if not category:
            raise CategoryForProductNotFound()

        # 2. Si se especifica un proveedor, verificar que exista
        supplier = None
        supplier_id = product_data.get("supplier_id")
        if supplier_id:
            supplier = self.supplier_repo.get_by_id(supplier_id)
            if not supplier:
                raise SupplierForProductNotFound()

        # 3. Verificar que el SKU no exista
        existing_product = self.product_repo.get_by_sku(product_data.get("sku"))
        if existing_product:
            raise ProductAlreadyExists()

        # 4. Build the rich domain object
        product_domain_obj = Product(
            **product_data, category=category, supplier=supplier
        )

        # 5. Crear el producto
        created_product = self.product_repo.create(product_domain_obj)
        return created_product
