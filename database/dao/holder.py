from sqlalchemy.ext.asyncio import AsyncSession

from database.dao.user import UserDAO


class DAO:
    """Holder data access object"""
    def __init__(self, session: AsyncSession):
        self.session = session

    @property
    def user(self):
        return UserDAO(self.session)