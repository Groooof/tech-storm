from contextlib import asynccontextmanager
from datetime import UTC, datetime
from typing import AsyncIterator, cast

import httpx
from fastapi import Depends, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from exceptions.auth import CredentialsException
from logic.auth import decode_access_token
from logic.users import get_user_by_id
from models.users import User
from schemas.auth import AccessTokenPayload
from shared.config import settings
from shared.utils import convert_database_url

async_engine = create_async_engine(convert_database_url(settings.database_url), echo=False)
http_bearer = HTTPBearer(auto_error=False)


async def get_httpx_client() -> AsyncIterator[httpx.AsyncClient]:
    async with httpx.AsyncClient() as client:
        yield client


async def get_session() -> AsyncIterator[AsyncSession]:
    async with AsyncSession(async_engine, expire_on_commit=False) as session:
        async with session.begin():
            async with session.begin_nested():
                yield session


@asynccontextmanager
async def _get_session() -> AsyncIterator[AsyncSession]:
    async with AsyncSession(async_engine, expire_on_commit=False) as session:
        async with session.begin():
            yield session


async def get_token(data: HTTPAuthorizationCredentials | None = Depends(http_bearer)) -> AccessTokenPayload:
    token_payload = cast(AccessTokenPayload | None, data and decode_access_token(data.credentials))
    if token_payload is None:
        raise CredentialsException(status_code=status.HTTP_401_UNAUTHORIZED, detail="INVALID_TOKEN")
    return token_payload


async def get_unexpired_token(
    token_payload: AccessTokenPayload = Depends(get_token),
) -> AccessTokenPayload | None:
    if token_payload.exp < datetime.now(UTC).timestamp():
        raise CredentialsException(status_code=status.HTTP_401_UNAUTHORIZED, detail='EXPIRED_TOKEN')
    return token_payload


async def get_current_user(
    session: AsyncSession = Depends(get_session), token_payload: AccessTokenPayload = Depends(get_token)
) -> User:
    user = await get_user_by_id(session, id=token_payload.user_id)
    if not user:
        raise CredentialsException(status_code=status.HTTP_401_UNAUTHORIZED, detail="INVALID_TOKEN")
    return user
