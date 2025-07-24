from typing import Optional
from src.domain.user import User
from src.interfaces.user_repository import UserRepository


class FakeUserRepository:
    def __init__(self):
        self.users = []
        self.id_counter = 1
        self.exist = 0

    def create(self, user: User) -> User:
        user.id = self.id_counter
        self.id_counter += 1
        self.users.append(user)
        return user

    def get_by_email(self, email: str) -> Optional[User]:
        return self.exist
