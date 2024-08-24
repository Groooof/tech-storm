from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import Base

if TYPE_CHECKING:
    from models.users import User


class UserRefreshToken(Base):
    __tablename__ = 'refresh_tokens'

    token: Mapped[UUID] = mapped_column(sa.UUID, primary_key=True)
    expires_at: Mapped[datetime] = mapped_column(sa.DateTime(timezone=True))
    user_id: Mapped[int] = mapped_column(sa.ForeignKey('users.id'))
    user: Mapped['User'] = relationship()
