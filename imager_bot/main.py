import logging
import time

import httpx
from telegram import Update, Message, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (ApplicationBuilder, CommandHandler, ContextTypes,
                          MessageHandler, filters, CallbackQueryHandler)
from whois import whois
from selenium.common.exceptions import SessionNotCreatedException
from imager_bot.config import settings
from imager_bot.services.driver import Browser

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


async def upload_image_telegraph(image: bytes) -> str:
    async with httpx.AsyncClient() as client:
        response = await client.post(
            url='https://telegra.ph/upload',
            files={'file': ('file', image, 'image/png')})
        if response.status_code == 200:
            json_ = response.json()[0]
            return json_.get("src")
        else:
            raise


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    start_ = time.time()
    url = update.message.text
    message: Message = await context.bot.send_message(chat_id=update.effective_chat.id,
                                                      text="⏳Запрос отправлен, ожидайте",
                                                      reply_to_message_id=update.message.message_id)
    try:
        page_data = Browser().get_screenshot(url)
        explained_time = time.time() - start_
        src = await upload_image_telegraph(page_data.screenshot)
        msg = (f"<b>{page_data.title}</b>\n\n"
               f"<b>Веб-сайт:</b> <a href='https://telegra.ph{src}'>&#160;</a>{url}\n"
               f"<b>Время обработки:</b> {explained_time:.2f}")

        keyboard = [
            [InlineKeyboardButton("🔍Подробнее", callback_data=url)],
        ]
        markup = InlineKeyboardMarkup(keyboard)
        await context.bot.edit_message_text(chat_id=update.effective_chat.id,
                                            message_id=message.message_id,
                                            text=msg,
                                            parse_mode="html",
                                            reply_markup=markup
                                            )
    except SessionNotCreatedException:
        await context.bot.edit_message_text(chat_id=update.effective_chat.id,
                                            message_id=message.message_id,
                                            text="Произошла ошибка",
                                            parse_mode="html",
                                            )


async def button(update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query
    w = whois(query.data)
    if isinstance(w.get('creation_date'), list):
        creation_date = w.get('creation_date')[0]
    else:
        creation_date = w.get('creation_date')
    if isinstance(w.get('expiration_date'), list):
        expiration_date = w.get('expiration_date')[0]
    else:
        expiration_date = w.get('expiration_date')

    info = (f"WHOIS:\n"
            f"Регистратор: {w.get('registrar')}\n"
            f"Зарегистрирован: {creation_date}\n"
            f"До: {expiration_date}\n"
            f"DNS-сервера:\n {w.get('name_servers')[-4:]} \n"
            f"Организация: {w.get('org')}\n"
            )
    await query.answer(show_alert=True, text=info[0:200])


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="I'm a bot, please talk to me!")


async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text="Sorry, I didn't understand that command.")


if __name__ == '__main__':
    application = ApplicationBuilder().token(settings.TG_BOT_TOKEN).build()
    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)
    start_handler = CommandHandler('start', start)
    unknown_handler = MessageHandler(filters.COMMAND, unknown)
    application.add_handler(start_handler)
    application.add_handler(unknown_handler)
    application.add_handler(echo_handler)
    application.add_handler(CallbackQueryHandler(button))
    application.run_polling()