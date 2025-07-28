from src.core.exceptions import AppException


class InsufficientStockError(AppException):
    def __init__(self):
        super().__init__(
            "Stock insuficiente para realizar la operación", status_code=409
        )


class StockMovementNotFound(AppException):
    def __init__(self):
        super().__init__("Movimiento de stock no encontrado", status_code=404)