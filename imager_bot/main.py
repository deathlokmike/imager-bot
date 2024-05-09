from loguru import logger
from telegram.ext import (ApplicationBuilder, CallbackQueryHandler,
                          CommandHandler, MessageHandler, filters)

from imager_bot import handlers
from imager_bot.config import settings

CALLBACK_QUERY_HANDLERS = {
    rf"^{settings.PATTERNS.CHOOSE_LANG_CALLBACK}$": handlers.choose_lang_button,
    rf"^{settings.PATTERNS.LANG_CALLBACK}\w{{2}}$": handlers.lang_button,
    rf"^{settings.PATTERNS.WHOIS_CALLBACK}(\S+)$": handlers.whois_button,
}

COMMAND_HANDLERS = {
    "start": handlers.start,
    "help": handlers.start
}

logger.add(
    sink="bot.json",
    rotation="1 week", compression="zip",
    level=settings.LOG_LEVEL,
    serialize=True
)


def main():
    logger.info("Start app")
    application = ApplicationBuilder().token(settings.TG_BOT_TOKEN).concurrent_updates(True).build()

    for command_name, command_handler in COMMAND_HANDLERS.items():
        application.add_handler(CommandHandler(command_name, command_handler))

    for pattern, handler in CALLBACK_QUERY_HANDLERS.items():
        application.add_handler(CallbackQueryHandler(handler, pattern=pattern))

    application.add_handler(
        MessageHandler(filters.TEXT & (~filters.COMMAND), handlers.take_screenshot)
    )

    application.add_handler(
        MessageHandler(filters.COMMAND, handlers.unknown))

    application.run_polling()


if __name__ == '__main__':
    try:
        main()
    except Exception:
        import traceback
        logger.warning(traceback.format_exc())
