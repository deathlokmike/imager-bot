from selenium.common.exceptions import WebDriverException
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from imager_bot.handlers.response import edit_text, send_text
from imager_bot.services.exceptions import UploadException, ValidationException
from imager_bot.services.screenshot import ScreenshotService
from imager_bot.services.types import ScreenshotData, ScreenshotMessageLocale

# from whois import whois


def _get_successful_response_template(
        locale: ScreenshotMessageLocale,
        screenshot_info: ScreenshotData) -> str:
    return (f"📎<b>{screenshot_info.title}</b>\n\n"
            f"🌐<b>{locale.website}:</b> <a href='{screenshot_info.img_source}'>&#160;</a>{screenshot_info.url}\n"
            f"⌛<b>{locale.process_time}:</b> {screenshot_info.explained_time:.2f}")


async def take_screenshot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        url = ScreenshotService.validate_url(update.message.text)
    except ValidationException:
        return

    locale = await ScreenshotService.get_locales(update.effective_user.id)
    message_id = await send_text(update, context, text="⏳" + locale.main, is_reply=True)

    try:
        screenshot_data = await ScreenshotService.get_data(url)
    except (UploadException, WebDriverException):
        await edit_text(update, context, text="🫣" + locale.error, message_id=message_id)
        return

    keyboard = [
        [InlineKeyboardButton("🔍" + locale.detail, callback_data=url)],
    ]
    markup = InlineKeyboardMarkup(keyboard)
    text = _get_successful_response_template(locale, screenshot_data)
    await edit_text(update, context, text=text, message_id=message_id, markup=markup)

# async def button(update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
#     query = update.callback_query
#     w = whois(query.data)
#     if isinstance(w.get('creation_date'), list):
#         creation_date = w.get('creation_date')[0]
#     else:
#         creation_date = w.get('creation_date')
#     if isinstance(w.get('expiration_date'), list):
#         expiration_date = w.get('expiration_date')[0]
#     else:
#         expiration_date = w.get('expiration_date')
#
#     info = (f"WHOIS:\n"
#             f"Регистратор: {w.get('registrar')}\n"
#             f"Зарегистрирован: {creation_date}\n"
#             f"До: {expiration_date}\n"
#             f"DNS-сервера:\n {w.get('name_servers')[-4:]} \n"
#             f"Организация: {w.get('org')}\n"
#             )
#     await query.answer(show_alert=True, text=info[0:200])
