import json

from telegram import (
    Update,
)
from telegram.ext import ContextTypes

from src.payments_aggregation import get_aggregated_payments


async def get_payments_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        params = json.loads(update.message.text)
    except json.decoder.JSONDecodeError:
        return await context.bot.send_message(
            chat_id=update.effective_chat.id, text="Invalid json"
        )

    date_upto = params.get("dt_upto")
    date_from = params.get("dt_from")
    group_type = params.get("group_type")

    try:
        aggregated_payments = get_aggregated_payments(date_from, date_upto, group_type)
    except Exception:
        return await context.bot.send_message(
            chat_id=update.effective_chat.id, text="error while getting data"
        )

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=json.dumps(aggregated_payments),
    )

    return "CONTACT_SHARE"
