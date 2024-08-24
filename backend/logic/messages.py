from sqlalchemy.ext.asyncio import AsyncSession

from schemas.messages import CreateMessageSchema, MessageData
from services.messages import MessagesService


async def get_user_messages(session: AsyncSession, user_id: int) -> list[MessageData]:
    service = MessagesService(session)
    return await service.get_user_messages(user_id)


async def create_message(session: AsyncSession, data: CreateMessageSchema) -> int:
    service = MessagesService(session)
    return await service.create_message(data)
