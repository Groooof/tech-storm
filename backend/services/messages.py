from sqlalchemy.ext.asyncio import AsyncSession

from models.messages import Message
from repositories.messages import MessagesRepository
from schemas.messages import CreateMessageSchema, MessageData


class MessagesService:
    def __init__(self, session: AsyncSession) -> None:
        self.messages_repo = MessagesRepository(session)

    async def get_user_messages(self, user_id: int) -> list[MessageData]:
        messages = await self.messages_repo.get_user_mesasges(user_id)
        return [
            MessageData(id=message.id, type_=message._type, text=message.text, created=message.created)
            for message in messages
        ]

    async def create_message(self, data: CreateMessageSchema) -> int:
        message = Message(_type=data.type_, text=data.text, user_id=data.user_id)
        await self.messages_repo.save(message)
        return message.id
