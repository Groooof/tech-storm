from sqlalchemy.ext.asyncio import AsyncSession

from schemas.auth import (
    AccessTokenPayload,
    LogoutSchema,
    RefreshTokensSchema,
    TokensSchema,
)
from services.auth import AccessTokenService, RefreshTokensService


def decode_access_token(token: str) -> AccessTokenPayload | None:
    return AccessTokenService().decode_token(token)


async def refresh_tokens(session: AsyncSession, data: RefreshTokensSchema) -> TokensSchema | None:
    new_access_token = AccessTokenService().create_token(data.user_id)
    new_refresh_token = await RefreshTokensService(session).refresh_token(data.refresh_token, data.user_id)
    if not new_refresh_token:
        return None
    return TokensSchema(access_token=new_access_token, refresh_token=new_refresh_token)


async def logout(session: AsyncSession, data: LogoutSchema) -> None:
    await RefreshTokensService(session).delete_token(data.refresh_token, data.user_id)
