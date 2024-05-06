from typing import Optional

from telegram import InlineKeyboardMarkup, Message, Update
from telegram.ext import ContextTypes


async def send_text(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
        text: str,
        markup: Optional[InlineKeyboardMarkup] = None,
        is_reply: bool = False) -> int:
    args = {
        "chat_id": update.effective_chat.id,
        "text": text,
        "parse_mode": "html"
    }
    if is_reply:
        args["reply_to_message_id"] = update.message.message_id
    if markup:
        args["reply_markup"] = markup

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
    await context.bot.edit_message_text(**args)
