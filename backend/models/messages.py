from datetime import datetime
from typing import TYPE_CHECKING

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from models.base import BaseWithId

if TYPE_CHECKING:
    from models.users import User


class Message(BaseWithId):
    __tablename__ = 'messages'

    _type: Mapped[str] = mapped_column(sa.String, name='type')  # [answer;question]
    text: Mapped[str] = mapped_column(sa.String)
    created: Mapped[datetime] = mapped_column(sa.DateTime(timezone=True), server_default=func.now())
    user_id: Mapped[int] = mapped_column(sa.ForeignKey('users.id'))
    user: Mapped['User'] = relationship()
