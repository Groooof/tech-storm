from datetime import UTC, datetime
from uuid import uuid4

import jwt
from sqlalchemy.ext.asyncio import AsyncSession

from repositories.auth import RefreshTokensRepository
from schemas.auth import AccessTokenPayload
from shared.config import settings


class RefreshTokensService:
    def __init__(self, session: AsyncSession) -> None:
        self.tokens_repo = RefreshTokensRepository(session)

    def generate_token(self) -> str:
        return str(uuid4())

    def get_token_expires(self) -> datetime:
        return datetime.now(UTC) + settings.users_refresh_token_lifetime

    async def create_token(self, user_id: int) -> str:
        token = self.generate_token()
        expires_at = self.get_token_expires()
        await self.tokens_repo.create_token(token, expires_at, user_id)
        return str(token)

    async def delete_token(self, token: str, user_id: int) -> None:
        await self.tokens_repo.delete_token(token, user_id)

    async def delete_all_tokens(self, user_id: int) -> None:
        await self.tokens_repo.delete_all_tokens(user_id)

    async def refresh_token(self, token: str, user_id: int) -> str | None:
        new_token = self.generate_token()
        new_expires_at = self.get_token_expires()
        res = await self.tokens_repo.update_if_exists(token, user_id, datetime.now(UTC), new_token, new_expires_at)
        if res:
            return str(new_token)
        return None


class AccessTokenService:
    def create_token(self, user_id: int) -> str:
        expires = datetime.now(UTC) + settings.users_access_token_lifetime
        payload = {'sub': user_id, 'exp': expires}
        return jwt.encode(payload, settings.secret_key)

    def decode_token(self, token: str) -> AccessTokenPayload | None:
        try:
            payload = jwt.decode(token, settings.secret_key, algorithms=['HS256'], options={'verify_exp': False})
        except jwt.exceptions.PyJWTError:
            return None
        return AccessTokenPayload(user_id=payload.get('sub'), exp=payload.get('exp'))
