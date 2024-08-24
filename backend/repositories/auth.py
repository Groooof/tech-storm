from datetime import datetime

from sqlalchemy import delete, update
from sqlalchemy.ext.asyncio import AsyncSession

from models.auth import UserRefreshToken


class RefreshTokensRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create_token(self, token: str, expires_at: datetime, user_id: int) -> None:
        token_obj = UserRefreshToken(token=token, expires_at=expires_at, user_id=user_id)
        self.session.add(token_obj)
        await self.session.flush()

    async def delete_token(self, token: str, user_id: int) -> None:
        stmt = delete(UserRefreshToken).where((UserRefreshToken.token == token) & (UserRefreshToken.user_id == user_id))
        await self.session.execute(stmt)

    async def delete_all_tokens(self, user_id: int) -> None:
        stmt = delete(UserRefreshToken).where(UserRefreshToken.user_id == user_id)
        await self.session.execute(stmt)

    async def update_if_exists(
        self, token: str, user_id: int, expires_at_from: datetime, new_token: str, new_expires_at: datetime
    ) -> str | None:
        stmt = (
            update(UserRefreshToken)
            .where(
                (UserRefreshToken.token == token)
                & (UserRefreshToken.user_id == user_id)
                & (UserRefreshToken.expires_at >= expires_at_from)
            )
            .values(token=new_token, expires_at=new_expires_at)
            .returning(UserRefreshToken.token)
        )
        return await self.session.scalar(stmt)
