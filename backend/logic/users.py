from sqlalchemy.ext.asyncio import AsyncSession

from models.users import User
from schemas.auth import TokensSchema
from schemas.users import UserAuthSchema, UserInfoSchema
from services.auth import AccessTokenService, RefreshTokensService
from services.users import UsersService


async def login_or_register_user(session: AsyncSession, data: UserAuthSchema) -> TokensSchema:
    service = UsersService(session)
    user = await service.authenticate_user(data)
    if not user:
        user = await service.register_user(data)

    access_token = AccessTokenService().create_token(user.id)
    refresh_token = await RefreshTokensService(session).create_token(user.id)
    return TokensSchema(access_token=access_token, refresh_token=refresh_token)


async def get_user_by_id(session: AsyncSession, id: int) -> User | None:
    return await UsersService(session).get_by_id(id)


async def get_user_info_by_id(session: AsyncSession, id: int) -> UserInfoSchema | None:
    return await UsersService(session).get_info_by_id(id)
