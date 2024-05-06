from typing import TYPE_CHECKING

from imager_bot.database.dao.stats import UsersStatisticsDaO
from imager_bot.database.dao.users import UsersDaO
from imager_bot.services.translator import Translator
from imager_bot.services.types import MessageLocale, StartMessageLocale

if TYPE_CHECKING:
    from imager_bot.database.models.users import Users


class UsersService:
    @classmethod
    async def _validate_user(cls, tg_id) -> "Users":
        user = await UsersDaO.get_by_id(tg_id)
        if not user:
            user = await UsersDaO.add(
                id=tg_id,
            )
            await UsersStatisticsDaO.add(
                id=tg_id,
            )
        return user

    @classmethod
    async def get_start_message(cls, tg_id: int) -> StartMessageLocale:
        user = await cls._validate_user(tg_id)
        await UsersStatisticsDaO.increase_start(tg_id)
        translator = Translator(user.locale)
        start_message_locale: StartMessageLocale = translator.get_translate("start", StartMessageLocale)

        return start_message_locale

    @classmethod
    async def get_choose_language_message(cls, tg_id: int) -> MessageLocale:
        user = await cls._validate_user(tg_id)
        translator = Translator(user.locale)
        message_locale: MessageLocale = translator.get_translate("choose_lang", MessageLocale)

        return message_locale

    @classmethod
    async def set_language(cls, tg_id: int, language: str):
        await cls._validate_user(tg_id)
        await UsersDaO.update_language(tg_id, language)
