from fastapi import APIRouter

from src.app.api.v1.routes.categories import router as categories_router
from src.app.api.v1.routes.products import router as products_router
from src.app.api.v1.routes.stock_movements import router as stock_movements_router
from src.app.api.v1.routes.suppliers import router as suppliers_router

router = APIRouter()

router.include_router(products_router)
router.include_router(categories_router)
router.include_router(suppliers_router)
router.include_router(stock_movements_router)