from sqlalchemy import update

from imager_bot.database.config import async_session
from imager_bot.database.dao.base import BaseDAO
from imager_bot.database.models.stats import UsersStatistics
from imager_bot.services.utils import naive_utcnow
from loguru import logger


class UsersStatisticsDaO(BaseDAO):
    model = UsersStatistics

    @classmethod
    async def add(cls, **data) -> UsersStatistics:
        data["start_date"] = naive_utcnow()
        data["last_message_date"] = naive_utcnow()
        logger.debug(f"Added new user: {data}")
        return await super().add(**data)

    @classmethod
    async def _increase_value(cls, tg_id: int, **arg):
        async with async_session() as session:
            query = (
                update(UsersStatistics)
                .filter(UsersStatistics.id == tg_id).
                values(**arg, last_message_date=naive_utcnow())
            )
        logger.debug(f"Execute: {query}")
        await session.execute(query)
        await session.commit()

    @classmethod
    async def increase_start(cls, tg_id: int):
        arg = {"start_message_count": UsersStatistics.__table__.c.start_message_count + 1}
        await cls._increase_value(tg_id, **arg)

    @classmethod
    async def increase_screenshot(cls, tg_id: int):
        arg = {"screenshot_message_count": UsersStatistics.__table__.c.screenshot_message_count + 1}
        await cls._increase_value(tg_id, **arg)

    @classmethod
    async def increase_bad_request(cls, tg_id: int):
        arg = {"bad_request_count": UsersStatistics.__table__.c.bad_request_count + 1}
        await cls._increase_value(tg_id, **arg)

    @classmethod
    async def increase_whois_request(cls, tg_id: int):
        arg = {"whois_request_count": UsersStatistics.__table__.c.whois_request_count + 1}
        await cls._increase_value(tg_id, **arg)
