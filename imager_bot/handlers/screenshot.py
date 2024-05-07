from selenium.common.exceptions import WebDriverException
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from imager_bot.config import settings
from imager_bot.handlers.response import edit_text, send_text
from imager_bot.services.exceptions import UploadException, ValidationException
from imager_bot.services.screenshot import ScreenshotService
from imager_bot.services.types import (ScreenshotData, ScreenshotMessageLocale)


def _get_successful_response_template(
        locale: ScreenshotMessageLocale,
        screenshot_data: ScreenshotData) -> str:
    return (f"📎<b>{screenshot_data.title}</b>\n\n"
            f"🌐<b>{locale.website}:</b> <a href='{screenshot_data.img_source}'>&#160;</a>{screenshot_data.url}\n"
            f"⌛<b>{locale.process_time}:</b> {screenshot_data.explained_time:.2f}")


async def take_screenshot(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        url = await ScreenshotService.get_url(update.message.text, update.effective_user.id)
    except ValidationException:
        return

    locale = await ScreenshotService.get_locales(update.effective_user.id)
    message_id = await send_text(update, context, text="⏳" + locale.main, is_reply=True)

    try:
        screenshot_data = await ScreenshotService.get_data(url, update.effective_user.id)
    except (UploadException, WebDriverException):
        await edit_text(update, context, text="🫣" + locale.error, message_id=message_id)
        return

    keyboard = [
        [InlineKeyboardButton("🔍" + locale.detail,
                              callback_data=settings.PATTERNS.WHOIS_CALLBACK + screenshot_data.domain)],
    ]
    markup = InlineKeyboardMarkup(keyboard)
    text = _get_successful_response_template(locale, screenshot_data)
    await edit_text(update, context, text=text, message_id=message_id, markup=markup)


async def whois_button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    if not query.data:
        return
    domain = _get_current_domain(query.data)
    text = await ScreenshotService.get_whois_data(domain, update.effective_user.id)
    await send_text(update, context, text)


def _get_current_domain(query_data) -> str:
    pattern_prefix_length = len(settings.PATTERNS.WHOIS_CALLBACK)
    return query_data[pattern_prefix_length:]
