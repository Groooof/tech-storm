from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from exceptions.users import WrongPasswordError
from logic.auth import logout as _logout, refresh_tokens
from logic.users import login_or_register_user as _login_or_register_user
from schemas.auth import (
    AccessTokenPayload,
    LogoutSchema,
    RefreshTokensRequestSchema,
    RefreshTokensSchema,
    TokensSchema,
)
from schemas.users import UserAuthSchema
from shared.dependencies import get_session, get_token

router = APIRouter(tags=['tokens'])


@router.post('/')
async def login_or_register_user(data: UserAuthSchema, session: AsyncSession = Depends(get_session)) -> TokensSchema:
    try:
        tokens = await _login_or_register_user(session, data)
    except WrongPasswordError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='WRONG_CREDENTIALS')
    return tokens


@router.post('/refresh', summary='Обновить токены')
async def refresh(
    data: RefreshTokensRequestSchema,
    session: AsyncSession = Depends(get_session),
    token: AccessTokenPayload = Depends(get_token),
) -> TokensSchema:
    new_tokens = await refresh_tokens(
        session,
        RefreshTokensSchema(
            user_id=token.user_id,
            refresh_token=data.refresh_token,
        ),
    )
    if not new_tokens:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='INVALID_TOKEN')
    return new_tokens


@router.post('/delete', summary='Выход')
async def logout(
    data: RefreshTokensRequestSchema,
    session: AsyncSession = Depends(get_session),
    token: AccessTokenPayload = Depends(get_token),
) -> None:
    await _logout(session, LogoutSchema(user_id=token.user_id, refresh_token=data.refresh_token))
