from fastapi import APIRouter
from src.app.api.v1.routes.products import router as products_router

router = APIRouter()

# Register the product routes
router.include_router(products_router)
