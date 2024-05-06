from sqlalchemy import insert

from imager_bot.database.config import async_session
from imager_bot.database.models.base import Base


class BaseDAO:
    model: Base

    @classmethod
    async def add(cls, **data):
        async with async_session() as session:
            query = insert(cls.model).values(**data)
            await session.execute(query)
            await session.commit()
