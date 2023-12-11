from functools import wraps

import anyio
from telegram._update import Update
from telegram.constants import ChatAction

from app.logs.api_logger import logging
from app.medium.medium_api import get_article_file
from app.telegram.models import TelegramConfig
from app.conf.configuration import config
import asyncio
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

conf = TelegramConfig(**config['tg_podolskowe_sprawy_bot'])

logger = logging.getLogger(__name__)

from telegram import Update
from telegram.ext import CommandHandler, MessageHandler, ConversationHandler, CallbackContext


def send_action(action):
    """Sends `action` while processing func command."""

    def decorator(func):
        @wraps(func)
        async def command_func(update, context, *args, **kwargs):
            await context.bot.send_chat_action(
                chat_id=update.effective_message.chat_id, action=action
            )
            return await func(update, context, *args, **kwargs)

        return command_func

    return decorator


# Stany maszyny stanów
AWAITING_MEDIUM_ID = 0


async def start_medium(update: Update, context: CallbackContext) -> int:
    await update.message.reply_text("Podaj link artykułu Medium:")
    logger.info(AWAITING_MEDIUM_ID)
    return AWAITING_MEDIUM_ID


@send_action(ChatAction.TYPING)
async def receive_medium_id(update: Update, context: CallbackContext) -> int:
    medium_url = update.message.text
    first_name = update.effective_user.first_name
    await update.message.reply_text(f"Dziękuję, {first_name}! Pobieram zawartość artykułu {medium_url}...")

    # Tutaj wykonaj zapytanie do API, aby uzyskać zawartość artykułu na podstawie ID
    # Przyjmijmy, że ta funkcja nazywa się get_medium_content
    try:
        medium_content = get_article_file(medium_url)
    except Exception as e:
        logger.error(e)
        medium_content = None

    if medium_content:
        # Wysyłamy zawartość artykułu jako plik do użytkownika
        await update.message.reply_document(document=medium_content, filename=medium_content)
    else:
        await update.message.reply_text("Nie udało się pobrać zawartości artykułu. Spróbuj ponownie.")

    # Resetujemy stan maszyny stanów
    return ConversationHandler.END


async def cancel(update: Update, context: CallbackContext) -> int:
    await update.message.reply_text("Anulowano.")
    return ConversationHandler.END


if __name__ == '__main__':
    application = ApplicationBuilder().token(conf.token).build()

    medium_handler = ConversationHandler(
        entry_points=[CommandHandler('medium', start_medium)],
        states={
            AWAITING_MEDIUM_ID: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_medium_id)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )
    application.add_handler(medium_handler)
    application.run_polling()
