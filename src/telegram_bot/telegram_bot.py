import logging
from src.telegram_bot.commands import get_payments_command
from src.telegram_bot.secrets import TELEGRAM_BOT_API_KEY
from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    filters,
)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

application = ApplicationBuilder().token(TELEGRAM_BOT_API_KEY).build()
payment_aggregation_handler = MessageHandler(filters.TEXT, get_payments_command)

application.add_handler(payment_aggregation_handler)


def start_bot():
    application.run_polling()
