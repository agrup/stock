from src.domain.user import User
from src.interfaces.user_repository import UserRepository
from src.core.user.exceptions import InvalidInput, UserAlreadyExists


class CreateUserUseCase:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    def execute(self, user: User) -> User:
        # Validaciones lógicas
        if len(user.name.strip().split()) < 2:
            raise InvalidInput("El nombre debe tener al menos dos palabras")

        if self.repo.get_by_email(user.email):
            raise UserAlreadyExists()

        return self.repo.create(user)
