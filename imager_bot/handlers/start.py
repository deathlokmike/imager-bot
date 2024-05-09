from loguru import logger
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from imager_bot.config import settings
from imager_bot.handlers.response import send_text
from imager_bot.services.translator import get_available_locales
from imager_bot.services.users import UsersService


async def get_start_locales_and_markup(update: Update):
    locales = await UsersService.get_start_message(update.effective_user.id)
    keyboard = [
        [InlineKeyboardButton(
            locales.choose_lang_button,
            callback_data=settings.PATTERNS.CHOOSE_LANG_CALLBACK)],
        [InlineKeyboardButton(
            locales.add_bot_to_group_button,
            callback_data=settings.PATTERNS.ADD_BOT_TO_GROUP_CALLBACK)],
    ]
    markup = InlineKeyboardMarkup(keyboard)
    return locales, markup


@logger.catch
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    locales, markup = await get_start_locales_and_markup(update)
    await send_text(update, context, locales.main, markup=markup)


@logger.catch
async def choose_lang_button(update: Update, _: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if not query.data:
        return
    available_locales = get_available_locales()
    keyboard = [
        [
            InlineKeyboardButton(available_locales[key],
                                 callback_data=settings.PATTERNS.LANG_CALLBACK + key) for key in available_locales
        ]
    ]
    locales = await UsersService.get_choose_language_message(update.effective_user.id)
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text=locales.main, reply_markup=reply_markup)


@logger.catch
async def lang_button(update: Update, _: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if not query.data:
        return

    current_lang = _get_current_lang(query.data)
    await UsersService.set_language(update.effective_user.id, current_lang)
    locales, reply_markup = await get_start_locales_and_markup(update)
    await query.edit_message_text(text=locales.main, reply_markup=reply_markup)


def _get_current_lang(query_data) -> str:
    pattern_prefix_length = len(settings.PATTERNS.LANG_CALLBACK)
    return query_data[pattern_prefix_length:]
