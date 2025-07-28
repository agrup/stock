from src.core.exceptions import AppException


class SupplierNotFound(AppException):
    def __init__(self):
        super().__init__("Proveedor no encontrado", status_code=404)


class SupplierAlreadyExists(AppException):
    def __init__(self):
        super().__init__("El proveedor con este nombre ya existe", status_code=409)


class SupplierInUseError(AppException):
    def __init__(self):
        super().__init__(
            "El proveedor está en uso y no puede ser eliminado", status_code=409
        )