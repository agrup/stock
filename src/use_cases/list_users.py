from src.interfaces.user_repository import UserRepository
from src.domain.user import User


class ListUsersUseCase:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    def execute(self) -> list[User]:
        return self.repo.list()
