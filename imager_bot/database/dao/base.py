from sqlalchemy import insert, select

from imager_bot.database.config import async_session
from imager_bot.database.models.base import Base


class BaseDAO:
    model: Base

    @classmethod
    async def add(cls, **data):
        async with async_session() as session:
            query = insert(cls.model).values(**data).returning(cls.model.__table__.columns)
            values = await session.execute(query)
            await session.commit()
            return values.mappings().one()

    @classmethod
    async def get_one_or_none(cls, **filter_by):
        async with async_session() as session:
            query = select(cls.model.__table__.columns).filter_by(**filter_by)
            result = await session.execute(query)
            return result.mappings().one_or_none()
