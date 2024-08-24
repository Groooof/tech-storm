from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.messages import Message
from repositories.generics import GenericSqlAlchemyRepository


class MessagesRepository(GenericSqlAlchemyRepository[Message]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(Message, session)

    async def get_user_mesasges(self, user_id: int) -> list[Message]:
        stmt = select(Message).where(Message.user_id == user_id).order_by(Message.created)
        return list(await self.session.scalars(stmt))
