from src.core.exceptions import AppException


class CategoryAlreadyExists(AppException):
    def __init__(self):
        super().__init__("La categoría con este nombre ya existe", status_code=409)