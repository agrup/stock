from fastapi import Depends
from sqlalchemy.orm import Session
from src.domain.user import User  # si lo necesitás
from src.repositories.sqlalchemy_user_repository import SqlAlchemyUserRepository
from src.use_cases.create_user import CreateUserUseCase
from src.infrastructure.sqlalchemy.session import (
    get_session,
)  # Asegúrate de que esta función esté definida en el archivo correcto
from src.use_cases.list_users import ListUsersUseCase


def get_sql_user_use_case(session: Session = Depends(get_session)) -> CreateUserUseCase:
    repo = SqlAlchemyUserRepository(session)
    return CreateUserUseCase(repo)


def get_list_users_use_case(
    session: Session = Depends(get_session),
) -> ListUsersUseCase:
    repo = SqlAlchemyUserRepository(session)
    return ListUsersUseCase(repo)
