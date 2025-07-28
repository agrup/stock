from src.core.product.exceptions import ProductNotFound
from src.core.stock_movements.exceptions import InsufficientStockError
from src.domain.stock_movement import StockMovement
from src.interfaces.product_repository import ProductRepository
from src.interfaces.stock_movement_repository import StockMovementRepository
from src.repositories.models.stock_movement import MovementType


class CreateStockMovementUseCase:
    def __init__(
        self,
        movement_repo: StockMovementRepository,
        product_repo: ProductRepository,
    ):
        self.movement_repo = movement_repo
        self.product_repo = product_repo

    def execute(self, movement_data: dict) -> StockMovement:
        product = self.product_repo.get_by_id(movement_data["product_id"])
        if not product:
            raise ProductNotFound()

        movement_type = movement_data["movement_type"]
        quantity = movement_data["quantity"]

        if movement_type == MovementType.ENTRADA:
            product.current_stock += quantity
        elif movement_type == MovementType.SALIDA:
            if product.current_stock < quantity:
                raise InsufficientStockError()
            product.current_stock -= quantity
        elif movement_type == MovementType.AJUSTE:
            product.current_stock = quantity

        # Actualizar el stock del producto en la BD
        self.product_repo.update(product.id, {"current_stock": product.current_stock})

        # Crear el movimiento de stock
        movement = StockMovement(**movement_data, product=product)
        created_movement = self.movement_repo.create(movement)
        return created_movement