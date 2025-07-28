from src.core.exceptions import AppException


class InsufficientStockError(AppException):
    def __init__(self):
        super().__init__(
            "Stock insuficiente para realizar la operación", status_code=409
        )