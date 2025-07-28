from src.core.product.exceptions import ProductNotFound
from src.core.stock_movements.exceptions import StockMovementNotFound
from src.interfaces.product_repository import ProductRepository
from src.interfaces.stock_movement_repository import StockMovementRepository
from src.repositories.models.stock_movement import MovementType


class DeleteStockMovementUseCase:
    def __init__(
        self,
        movement_repo: StockMovementRepository,
        product_repo: ProductRepository,
    ):
        self.movement_repo = movement_repo
        self.product_repo = product_repo

    def execute(self, movement_id: int) -> None:
        movement_to_delete = self.movement_repo.get_by_id(movement_id)
        if not movement_to_delete:
            raise StockMovementNotFound()

        product = self.product_repo.get_by_id(movement_to_delete.product_id)
        if not product:
            # This indicates data inconsistency, but we handle it gracefully.
            raise ProductNotFound()

        # Revert the stock change based on the movement type
        if movement_to_delete.movement_type == MovementType.ENTRADA:
            product.current_stock -= movement_to_delete.quantity
        elif movement_to_delete.movement_type == MovementType.SALIDA:
            product.current_stock += movement_to_delete.quantity

        self.product_repo.update(product.id, {"current_stock": product.current_stock})

        self.movement_repo.delete(movement_id)