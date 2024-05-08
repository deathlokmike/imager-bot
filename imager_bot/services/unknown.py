from imager_bot.database.dao.stats import UsersStatisticsDaO
from imager_bot.database.dao.users import UsersDaO
from imager_bot.services.translator import Translator
from imager_bot.services.types import MessageLocale


async def get_unknown_message_locale(tg_id: int) -> MessageLocale:
    user = await UsersDaO.get_by_id(tg_id)
    await UsersStatisticsDaO.increase_bad_request(tg_id)
    translator = Translator(user.locale)
    locale: MessageLocale = translator.get_translate("unknown_command", MessageLocale)
    return locale
