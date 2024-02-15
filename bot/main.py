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

# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger('httpx').setLevel(logging.WARNING)

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
    """
    This function save a set in the database.
    """
    if context.args:
        args_str = ' '.join(context.args)
        try:
            exercise_name, reps, weight = [
                arg.strip() for arg in args_str.split(',')
            ]

            reps = int(reps)
            weight = float(weight)
            load = reps * weight
            # TODO: save this in a database with date and user_id
            message = (
                f'Successfully registered:\n'
                f'{exercise_name}\n'
                f'{reps} reps - {weight}kg\n'
                f'Load - {load}'
            )

        except ValueError as e:
            logger.error(f'Error processing arguments: {e}')
            message = 'Error processing your request. Please use the format: /set Exercise Name, Repetitions, Weight(kg)'
    else:
        # If has no args
        message = 'Please provide the exercise details in the format: /set Exercise Name, Repetitions, Weight (kg)'

    await context.bot.send_message(
        chat_id=update.effective_chat.id, text=message
    )


async def exercise_register(
    update: Update, context: ContextTypes.DEFAULT_TYPE
):
    """
    This function save varios sets of an exercise in the database.
    """
    pass


async def workout_register(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    This function save a full workout in the database.
    """
    pass


async def today_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    This function returns the today status, broken down by set and total of the workout.
    """
    pass


async def stats_by_day(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    This function returns the status of the day, broken down by set and total of the workout.
    """
    pass


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
    start_handler = CommandHandler('start', start)

    application.add_handler(echo_handler)
    application.add_handler(set_handler)
    application.add_handler(start_handler)

    # Start app until killed
    application.run_polling()


if __name__ == '__main__':
    main()
