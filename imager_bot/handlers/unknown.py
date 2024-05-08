from telegram import Update
from telegram.ext import ContextTypes

from imager_bot.handlers.response import send_text
from imager_bot.services.unknown import get_unknown_message_locale


async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    locale = await get_unknown_message_locale(update.effective_user.id)
    await send_text(update, context, text="🙅‍♂️" + locale.main)
