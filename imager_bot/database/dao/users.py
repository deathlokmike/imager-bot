from typing import Optional

from sqlalchemy import update

from imager_bot.database.config import async_session
from imager_bot.database.dao.base import BaseDAO
from imager_bot.database.models.users import Users


class UsersDaO(BaseDAO):
    model = Users

    @classmethod
    async def add(cls, **data) -> Users:
        return await super().add(**data)

    @classmethod
    async def get_by_id(cls, tg_id: int) -> Optional[Users]:
        return await cls.get_one_or_none(id=tg_id)

    @classmethod
    async def update_language(cls, tg_id: int, language: str):
        async with async_session() as session:
            query = (
                update(Users)
                .filter(Users.id == tg_id)
                .ordered_values(
                    (Users.locale, language)
                )
            )
        await session.execute(query)
        await session.commit()
