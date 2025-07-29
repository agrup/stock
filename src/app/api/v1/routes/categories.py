from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException, status

from src.app.dependencies.category_use_cases import category_container
from src.app.dependencies.common_filters import PaginationParams, get_pagination_params
from src.core.category.exceptions import (
    CategoryAlreadyExists,
    CategoryInUseError,
    CategoryNotFound,
)
from src.domain.category import Category
from src.schemas.category import (
    CreateCategorySchema,
    CategoryResponseSchema,
    UpdateCategorySchema,
)
from src.use_cases.create_category import CreateCategoryUseCase
from src.use_cases.get_all_categories import GetAllCategoriesUseCase
from src.use_cases.get_category_by_id import GetCategoryByIdUseCase
from src.use_cases.update_category import UpdateCategoryUseCase
from src.use_cases.delete_category import DeleteCategoryUseCase

router = APIRouter(prefix="/categories", tags=["Categories"])


@router.post(
    "/", response_model=CategoryResponseSchema, status_code=status.HTTP_201_CREATED
)
def create_category(
    category_data: CreateCategorySchema,
    use_case: Annotated[
        CreateCategoryUseCase, Depends(category_container.create_category)
    ],
):
    try:
        category = Category(**category_data.model_dump())
        created_category = use_case.execute(category)
        return created_category
    except CategoryAlreadyExists as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)


@router.get("/", response_model=List[CategoryResponseSchema])
def get_all_categories(
    commons: Annotated[PaginationParams, Depends(get_pagination_params)],
    use_case: Annotated[
        GetAllCategoriesUseCase, Depends(category_container.get_all_categories)
    ],
):
    categories = use_case.execute(commons)
    return categories


@router.get("/{category_id}", response_model=CategoryResponseSchema)
def get_category_by_id(
    category_id: int,
    use_case: Annotated[
        GetCategoryByIdUseCase, Depends(category_container.get_category_by_id)
    ],
):
    try:
        return use_case.execute(category_id)
    except CategoryNotFound as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)


@router.put("/{category_id}", response_model=CategoryResponseSchema)
def update_category(
    category_id: int,
    category_data: UpdateCategorySchema,
    use_case: Annotated[
        UpdateCategoryUseCase, Depends(category_container.update_category)
    ],
):
    try:
        return use_case.execute(
            category_id, category_data.model_dump(exclude_unset=True)
        )
    except (CategoryNotFound, CategoryAlreadyExists) as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(
    category_id: int,
    use_case: Annotated[
        DeleteCategoryUseCase, Depends(category_container.delete_category)
    ],
):
    try:
        use_case.execute(category_id)
    except (CategoryNotFound, CategoryInUseError) as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
