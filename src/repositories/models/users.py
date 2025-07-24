from sqlalchemy.orm import Mapped, mapped_column
from src.infrastructure.sqlalchemy.base import Base

from sqlalchemy import String


class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255))
    email: Mapped[str] = mapped_column(String(255), unique=True)
