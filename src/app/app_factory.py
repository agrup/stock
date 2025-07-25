from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from src.core.exceptions import AppException
from src.app.api.v1.router import router
def create_app() -> FastAPI:
    app = FastAPI(title="My Clean App")

    # Rutas
    app.include_router(router, prefix="/v1")

    # Manejador global de errores personalizados
    @app.exception_handler(AppException)
    async def handle_app_exception(_: Request, exc: AppException):
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.message},  # usar 'detail' por convención
        )

    # Errores de validación (Pydantic)
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(_: Request, exc: RequestValidationError):
        return JSONResponse(
            status_code=422,
            content={"detail": exc.errors()},
        )

    # Errores HTTP estándar (404, 405, etc)
    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(_: Request, exc: StarletteHTTPException):
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail},
        )

    return app
