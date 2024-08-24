from sqlalchemy.ext.asyncio import AsyncSession

from exceptions.users import WrongPasswordError
from models.users import User
from repositories.users import UsersRepository
from schemas.users import UserAuthSchema, UserInfoSchema


class UsersService:
    def __init__(self, session: AsyncSession) -> None:
        self.users_repo = UsersRepository(session)

    async def authenticate_user(self, data: UserAuthSchema) -> User | None:
        user = await self.users_repo.get_by_username(username=data.username)
        if user and user.password != data.password:
            raise WrongPasswordError
        return user

    async def register_user(self, data: UserAuthSchema) -> User:
        user = User(username=data.username, password=data.password)
        await self.users_repo.save(user)
        return user

    async def get_by_id(self, id: int) -> User | None:
        return await self.users_repo.get_by_id(id)

    async def get_info_by_id(self, id: int) -> UserInfoSchema | None:
        user = await self.users_repo.get_by_id(id)
        return UserInfoSchema(id=user.id, username=user.username) if user else None
