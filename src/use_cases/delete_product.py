from src.core.product.exceptions import ProductNotFound
from src.interfaces.product_repository import ProductRepository


class DeleteProductUseCase:
    def __init__(self, product_repo: ProductRepository):
        self.product_repo = product_repo

    def execute(self, product_id: int) -> None:
        # 1. Verificar que el producto a eliminar exista
        product_to_delete = self.product_repo.get_by_id(product_id)
        if not product_to_delete:
            raise ProductNotFound()

        # 2. Eliminar el producto
        self.product_repo.delete(product_id)
