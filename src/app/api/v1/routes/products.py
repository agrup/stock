from typing import List
from fastapi import APIRouter, Depends, HTTPException, status

from src.app.dependencies.product_use_cases import (
    product_container,
)
from src.core.product.exceptions import CategoryNotFound, ProductAlreadyExists, ProductNotFound
from src.domain.product import Product
from src.schemas.product import CreateProductSchema, ProductResponseSchema, UpdateProductSchema
from src.use_cases.create_product import CreateProductUseCase
from src.use_cases.get_all_products import GetAllProductsUseCase
from src.use_cases.get_product_by_id import GetProductByIdUseCase
from src.use_cases.update_product import UpdateProductUseCase

router = APIRouter(prefix="/products", tags=["Products"])


@router.post(
    "/",
    response_model=ProductResponseSchema,
    status_code=status.HTTP_201_CREATED,
)
def create_product(
    product_data: CreateProductSchema,
    use_case: CreateProductUseCase = Depends(product_container.create_product),
):
    try:
        product = Product(**product_data.model_dump())
        created_product = use_case.execute(product)
        return created_product
    except (ProductAlreadyExists, CategoryNotFound) as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)


@router.get("/", response_model=List[ProductResponseSchema])
def get_all_products(
    use_case: GetAllProductsUseCase = Depends(product_container.get_all_products),
):
    products = use_case.execute()
    return products


@router.get("/{product_id}", response_model=ProductResponseSchema)
def get_product_by_id(
    product_id: int,
    use_case: GetProductByIdUseCase = Depends(product_container.get_product_by_id),
):
    try:
        product = use_case.execute(product_id)
        return product
    except ProductNotFound as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)


@router.put("/{product_id}", response_model=ProductResponseSchema)
def update_product(
    product_id: int,
    product_data: UpdateProductSchema,
    use_case: UpdateProductUseCase = Depends(product_container.update_product),
):
    try:
        # Usamos exclude_unset para no enviar campos None al caso de uso
        updated_product = use_case.execute(
            product_id, product_data.model_dump(exclude_unset=True)
        )
        return updated_product
    except (ProductNotFound, CategoryNotFound, ProductAlreadyExists) as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)