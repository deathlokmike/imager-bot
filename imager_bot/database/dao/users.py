from typing import Optional

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
