from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    MessageHandler,
    filters,
)
import logging
import os

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
)

logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!"
    )


# Function to reply a message in CAPS
async def caps(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text_caps = ' '.join(context.args).upper()
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text=text_caps
    )


# Function echo - reply same text if its not a command
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text=update.message.text
    )


# Main function to run bot
def main() -> None:
    # Load token
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    if not token:
        logger.error(
            'Token not found. Make sure the environment variable is defined.'
        )
        return

    application = ApplicationBuilder().token(token).build()

    # Register the commands
    start_handler = CommandHandler('start', start)
    caps_handler = CommandHandler('caps', caps)
    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)

    application.add_handler(echo_handler)
    application.add_handler(caps_handler)
    application.add_handler(start_handler)

    # Start app until killed
    application.run_polling()


if __name__ == '__main__':
    main()
