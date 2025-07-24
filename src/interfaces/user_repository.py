from typing import Optional, Protocol, runtime_checkable
from src.domain.user import User


@runtime_checkable
class UserRepository(Protocol):
    def create(self, user: User) -> User: ...

    def list(self) -> list[User]: ...

    def get_by_email(self, email: str) -> Optional[User]: ...
