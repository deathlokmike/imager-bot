from typing import Optional

from loguru import logger
from telegram import InlineKeyboardMarkup, Message, Update
from telegram.ext import ContextTypes


async def send_text(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
        text: str,
        markup: Optional[InlineKeyboardMarkup] = None,
        is_reply=False,
        enable_parse_mode=True) -> int:
    args = {
        "chat_id": update.effective_chat.id,
        "text": text,
    }
    if is_reply:
        args["reply_to_message_id"] = update.message.message_id
    if markup:
        args["reply_markup"] = markup
    if enable_parse_mode:
        args["parse_mode"] = "html"
    logger.debug(f"Send message to {update.effective_user.id}: {text}")
    message: Message = await context.bot.send_message(**args)
    return message.message_id


async def edit_text(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
        text: str,
        message_id: int,
        markup: Optional[InlineKeyboardMarkup] = None,
):
    args = {
        "chat_id": update.effective_chat.id,
        "message_id": message_id,
        "text": text,
        "parse_mode": "html"
    }
    if markup:
        args["reply_markup"] = markup
    logger.debug(f"Edit message to {update.effective_user.id}: {text}")
    await context.bot.edit_message_text(**args)
