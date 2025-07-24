from typing import Optional
from src.repositories.models.users import UserModel
from src.domain.user import User
from src.interfaces.user_repository import UserRepository
from sqlalchemy.orm import Session


class SqlAlchemyUserRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, user: User) -> User:
        user_model = UserModel(name=user.name, email=user.email)
        self.session.add(user_model)
        self.session.commit()
        self.session.refresh(user_model)
        return User(id=user_model.id, name=user_model.name, email=user_model.email)

    def list(self) -> list[User]:
        users = self.session.query(UserModel).all()
        return [User(id=u.id, name=u.name, email=u.email) for u in users]

    def get_by_email(self, email: str) -> Optional[User]:
        user = self.session.query(UserModel).filter_by(email=email).first()
        if not user:
            return None
        return User(id=user.id, name=user.name, email=user.email)
