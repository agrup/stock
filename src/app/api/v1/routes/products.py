from typing import List, Annotated
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
from src.use_cases.delete_product import DeleteProductUseCase

router = APIRouter(prefix="/products", tags=["Products"])


@router.post(
    "/",
    response_model=ProductResponseSchema,
    status_code=status.HTTP_201_CREATED,
)
def create_product(
    product_data: CreateProductSchema,
    use_case: Annotated[CreateProductUseCase, Depends(product_container.create_product)],
):
    try:
        product = Product(**product_data.model_dump())
        created_product = use_case.execute(product)
        return created_product
    except (ProductAlreadyExists, CategoryNotFound) as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)


@router.get("/", response_model=List[ProductResponseSchema])
def get_all_products(
    use_case: Annotated[GetAllProductsUseCase, Depends(product_container.get_all_products)],
):
    products = use_case.execute()
    return products


@router.get("/{product_id}", response_model=ProductResponseSchema)
def get_product_by_id(
    product_id: int,
    use_case: Annotated[GetProductByIdUseCase, Depends(product_container.get_product_by_id)],
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
    use_case: Annotated[UpdateProductUseCase, Depends(product_container.update_product)],
):
    try:
        # Usamos exclude_unset para no enviar campos None al caso de uso
        updated_product = use_case.execute(
            product_id, product_data.model_dump(exclude_unset=True)
        )
        return updated_product
    except (ProductNotFound, CategoryNotFound, ProductAlreadyExists) as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(
    product_id: int,
    use_case: Annotated[DeleteProductUseCase, Depends(product_container.delete_product)],
):
    try:
        use_case.execute(product_id)
        return None # No se devuelve contenido en un 204
    except ProductNotFound as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)