from datetime import datetime

from pydantic import BaseModel


class MessageData(BaseModel):
    id: int
    type_: str  # [answer;question]
    text: str
    created: datetime


class CreateMessageSchema(BaseModel):
    user_id: int
    type_: str  # [answer;question]
    text: str
