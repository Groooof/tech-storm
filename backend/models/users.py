import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy_utils import PasswordType

from models.base import BaseWithId


class User(BaseWithId):
    __tablename__ = 'users'

    username: Mapped[str] = mapped_column(sa.String)
    password: Mapped[str] = mapped_column(PasswordType(schemes=['pbkdf2_sha512']))

    def __str__(self) -> str:
        return f'User: {self.username}'
