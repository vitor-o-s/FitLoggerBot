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
    user = update.effective_user.first_name
    message = (
        f'Hello {user}, I am a bot. Please let me help with your training!\n'
        'If you want:\n'
        '1 - Register one set type: /set\n'
        '2 - Help: /help'
    )

    await context.bot.send_message(
        chat_id=update.effective_chat.id, text=message
    )


async def set_register(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = 'Successfully registered series!'
    logger.info(type(update.message.text))
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text=message
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
    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)
    set_handler = CommandHandler('set', set_register)
    caps_handler = CommandHandler('caps', caps)
    start_handler = CommandHandler('start', start)

    application.add_handler(echo_handler)
    application.add_handler(set_handler)
    application.add_handler(caps_handler)
    application.add_handler(start_handler)

    # Start app until killed
    application.run_polling()


if __name__ == '__main__':
    main()
