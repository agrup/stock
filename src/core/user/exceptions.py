class AppException(Exception):
    """Base de errores personalizados."""

    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code
        super().__init__(message)


class UserAlreadyExists(AppException):
    def __init__(self):
        super().__init__("El usuario ya existe", status_code=409)


class UserNotFound(AppException):
    def __init__(self):
        super().__init__("Usuario no encontrado", status_code=404)


class InvalidInput(AppException):
    def __init__(self, message: str):
        super().__init__(message, status_code=422)
