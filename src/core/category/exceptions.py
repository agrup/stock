from src.core.exceptions import AppException


class CategoryAlreadyExists(AppException):
    def __init__(self):
        super().__init__("La categoría con este nombre ya existe", status_code=409)


class CategoryNotFound(AppException):
    def __init__(self):
        super().__init__("Categoría no encontrada", status_code=404)


class CategoryInUseError(AppException):
    def __init__(self):
        super().__init__("La categoría está en uso y no puede ser eliminada", status_code=409)