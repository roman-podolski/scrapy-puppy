import anyio
from telegram._update import Update
from app.logs.api_logger import logger
from app.telegram.models import TelegramConfig
from app.conf.configuration import config
import asyncio
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler,MessageHandler, filters

conf = TelegramConfig(**config['tg_podolskowe_sprawy_bot'])


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f"Received start command from {update.effective_user.first_name}")
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message.text
    logger.info(f"Received message: {message}")
    await context.bot.send_message(chat_id=update.effective_chat.id, text=message)

async def medium(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f"Received start command from {update.effective_user.first_name}")
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Give me a medium article id")
    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)
    ids = application.add_handler(echo_handler)
    await anyio.sleep(5)
    logger.info(f"Handler id: {ids}")


if __name__ == '__main__':
    application = ApplicationBuilder().token(conf.token).build()

    start_handler = CommandHandler('start', start)
    medium_handler = CommandHandler('medium', medium)
    application.add_handler(start_handler)
    application.add_handler(medium_handler)

    application.run_polling()