from sqlalchemy.ext.asyncio import AsyncSession

from database.dao.base import BaseDAO
from database.models import User


class UserDAO(BaseDAO[User]):
    def __init__(self, session: AsyncSession):
        super().__init__(User, session)

    async def create(self, chat_id: int, username: str) -> User:
        user = await self.session.merge(User(id=chat_id, username=username))
        await self.commit()
        return user
