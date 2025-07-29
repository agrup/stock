from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException, status

from src.app.dependencies.supplier_use_cases import supplier_container
from src.app.dependencies.common_filters import PaginationParams, get_pagination_params
from src.core.suppliers.exceptions import (
    SupplierAlreadyExists,
    SupplierInUseError,
    SupplierNotFound,
)
from src.domain.supplier import Supplier
from src.schemas.supplier import (
    CreateSupplierSchema,
    SupplierResponseSchema,
    UpdateSupplierSchema,
)
from src.use_cases.create_supplier import CreateSupplierUseCase
from src.use_cases.delete_supplier import DeleteSupplierUseCase
from src.use_cases.get_all_suppliers import GetAllSuppliersUseCase
from src.use_cases.get_supplier_by_id import GetSupplierByIdUseCase
from src.use_cases.update_supplier import UpdateSupplierUseCase

router = APIRouter(prefix="/suppliers", tags=["Suppliers"])


@router.post(
    "/", response_model=SupplierResponseSchema, status_code=status.HTTP_201_CREATED
)
def create_supplier(
    supplier_data: CreateSupplierSchema,
    use_case: Annotated[
        CreateSupplierUseCase, Depends(supplier_container.create_supplier)
    ],
):
    try:
        supplier = Supplier(**supplier_data.model_dump())
        return use_case.execute(supplier)
    except SupplierAlreadyExists as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)


@router.get("/", response_model=List[SupplierResponseSchema])
def get_all_suppliers(
    commons: Annotated[PaginationParams, Depends(get_pagination_params)],
    use_case: Annotated[
        GetAllSuppliersUseCase, Depends(supplier_container.get_all_suppliers)
    ],
):
    return use_case.execute(commons)


@router.get("/{supplier_id}", response_model=SupplierResponseSchema)
def get_supplier_by_id(
    supplier_id: int,
    use_case: Annotated[
        GetSupplierByIdUseCase, Depends(supplier_container.get_supplier_by_id)
    ],
):
    try:
        return use_case.execute(supplier_id)
    except SupplierNotFound as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)


@router.put("/{supplier_id}", response_model=SupplierResponseSchema)
def update_supplier(
    supplier_id: int,
    supplier_data: UpdateSupplierSchema,
    use_case: Annotated[
        UpdateSupplierUseCase, Depends(supplier_container.update_supplier)
    ],
):
    try:
        update_payload = supplier_data.model_dump(exclude_unset=True)
        return use_case.execute(supplier_id, update_payload)
    except (SupplierNotFound, SupplierAlreadyExists) as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)


@router.delete("/{supplier_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_supplier(
    supplier_id: int,
    use_case: Annotated[
        DeleteSupplierUseCase, Depends(supplier_container.delete_supplier)
    ],
):
    try:
        use_case.execute(supplier_id)
    except (SupplierNotFound, SupplierInUseError) as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)