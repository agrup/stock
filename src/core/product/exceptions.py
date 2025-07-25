
from src.core.exceptions import AppException


class ProductAlreadyExists(AppException):
    def __init__(self):
        super().__init__("El producto con este SKU ya existe", status_code=409)


class CategoryNotFound(AppException):
    def __init__(self):
        super().__init__("La categoría especificada no existe", status_code=404)


class ProductNotFound(AppException):
    def __init__(self):
        super().__init__("Producto no encontrado", status_code=404)