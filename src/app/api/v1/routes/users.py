from fastapi import APIRouter, Depends
from src.domain.user import User
from src.schemas.user import CreateUserSchema, UserResponseSchema
from src.use_cases.create_user import CreateUserUseCase
from src.app.dependencies.user_use_cases import get_sql_user_use_case
from src.use_cases.list_users import ListUsersUseCase
from src.app.dependencies.user_use_cases import get_list_users_use_case

router = APIRouter()


@router.post("/users")
def create_user(
    user: CreateUserSchema, use_case: CreateUserUseCase = Depends(get_sql_user_use_case)
):
    return use_case.execute(User(**user.model_dump()))


@router.get("/users", response_model=list[User])
def list_users(use_case: ListUsersUseCase = Depends(get_list_users_use_case)):
    return use_case.execute()
