from fastapi import APIRouter, Depends, HTTPException, status

from src.app.dependencies.product_use_cases import get_create_product_use_case
from src.core.product.exceptions import ProductAlreadyExists
from src.domain.product import Product
from src.schemas.product import CreateProductSchema, ProductResponseSchema
from src.use_cases.create_product import CreateProductUseCase

router = APIRouter(prefix="/products", tags=["Products"])


@router.post(
    "/",
    response_model=ProductResponseSchema,
    status_code=status.HTTP_201_CREATED,
)
def create_product(
    product_data: CreateProductSchema,
    use_case: CreateProductUseCase = Depends(get_create_product_use_case),
):
    try:
        product = Product(**product_data.model_dump())
        created_product = use_case.execute(product)
        return created_product
    except ProductAlreadyExists as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)