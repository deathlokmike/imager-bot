from sqlalchemy import update

from imager_bot.database.config import async_session
from imager_bot.database.dao.base import BaseDAO
from imager_bot.database.models.stats import UsersStatistics
from imager_bot.database.utils import naive_utcnow


class UsersStatisticsDaO(BaseDAO):
    model = UsersStatistics

    @classmethod
    async def add(cls, **data) -> UsersStatistics:
        data["start_date"] = naive_utcnow()
        data["last_message_date"] = naive_utcnow()
        return await super().add(**data)

    @classmethod
    async def increase_start(cls, tg_id):
        async with async_session() as session:
            query = (
                update(UsersStatistics)
                .filter(UsersStatistics.id == tg_id).
                values(start_message_count=UsersStatistics.__table__.c.start_message_count + 1,
                       last_message_date=naive_utcnow())
            )
        await session.execute(query)
        await session.commit()