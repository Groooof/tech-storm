from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.users import User
from repositories.generics import GenericSqlAlchemyRepository


class UsersRepository(GenericSqlAlchemyRepository[User]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(User, session)

    async def get_by_username(self, username: str) -> User | None:
        stmt = select(self.model).where(User.username == username)
        return await self.session.scalar(stmt)
