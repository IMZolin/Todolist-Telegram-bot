from typing import TypeVar, Generic, Type, List, Any

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Load

from database.models.base import Base

Model = TypeVar('Model', Base, Base)


class BaseDAO(Generic[Model]):
    """Base data access object"""

    def __init__(self, model: Type[Model], session: AsyncSession):
        self.model = model
        self.session = session

    async def get_by_id(self, id_: Any, options: list[Load] = None) -> Model:
        return await self.session.get(self.model, id_, options=options)

    async def get_all(self) -> List[Model]:
        result = await self.session.execute(select(self.model))
        return result.scalars().all()

    async def count(self):
        result = await self.session.execute(select(func.count(self.model.id)))
        return result.scalar_one()

    async def delete(self, obj: Model):
        await self.session.delete(obj)

    async def commit(self):
        await self.session.commit()

    def save(self, obj: Model):
        self.session.add(obj)

    async def flush(self, *objects):
        await self.session.flush(objects)
