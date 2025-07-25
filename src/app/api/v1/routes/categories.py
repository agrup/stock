from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException, status

from src.app.dependencies.category_use_cases import category_container
from src.core.category.exceptions import CategoryAlreadyExists
from src.domain.category import Category
from src.schemas.category import CreateCategorySchema, CategoryResponseSchema
from src.use_cases.create_category import CreateCategoryUseCase
from src.use_cases.get_all_categories import GetAllCategoriesUseCase

router = APIRouter(prefix="/categories", tags=["Categories"])


@router.post("/", response_model=CategoryResponseSchema, status_code=status.HTTP_201_CREATED)
def create_category(
    category_data: CreateCategorySchema,
    use_case: Annotated[CreateCategoryUseCase, Depends(category_container.create_category)],
):
    try:
        category = Category(**category_data.model_dump())
        created_category = use_case.execute(category)
        return created_category
    except CategoryAlreadyExists as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)


@router.get("/", response_model=List[CategoryResponseSchema])
def get_all_categories(
    use_case: Annotated[GetAllCategoriesUseCase, Depends(category_container.get_all_categories)],
):
    categories = use_case.execute()
    return categories