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
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="invalid json"
        )
        return

    date_upto = params.get("dt_upto")
    date_from = params.get("dt_from")
    group_type = params.get("group_type")

    aggregated_payments = get_aggregated_payments(date_from, date_upto, group_type)

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=json.dumps(aggregated_payments),
    )

    return "CONTACT_SHARE"
