from typing import Any, Generic, TypeVar

from sqlalchemy import Select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.expression import select

from models.base import BaseWithId

ModelType = TypeVar("ModelType", bound=BaseWithId, contravariant=True)


class GenericSqlAlchemyRepository(Generic[ModelType]):
    def __init__(self, model: type[ModelType], session: AsyncSession) -> None:
        self.model = model
        self.session = session

    async def save(self, obj: ModelType) -> None:
        self.session.add(obj)
        await self.session.flush()

    async def get_by_id(self, id: int) -> ModelType | None:
        stmt: Select = select(self.model).where(self.model.id == id)
        return (await self.session.execute(stmt)).scalar()

    async def update_by_id(self, id: int, **values: Any) -> None:
        stmt = update(self.model).where(self.model.id == id).values(**values)
        await self.session.execute(stmt)
        await self.session.flush()

    async def list(self) -> list[ModelType]:
        stmt: Select = select(self.model)
        return list((await self.session.execute(stmt)).scalars())
