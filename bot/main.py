from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    MessageHandler,
    filters,
)
from db import save_workout
import logging
import os
from datetime import datetime, timedelta

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
)

# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger('httpx').setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user.first_name
    chat_id = update.effective_chat.id
    chat_data = context.chat_data

    # Start session
    chat_data['session_active'] = True
    chat_data['last_activity'] = datetime.utcnow().isoformat()

    # Cancel any existing timeout job
    prev_job = chat_data.get('session_job')
    if prev_job:
        try:
            prev_job.schedule_removal()
        except Exception:
            pass

    # Schedule timeout
    job = context.application.job_queue.run_once(
        _session_timeout, when=timedelta(minutes=60), chat_id=chat_id
    )
    chat_data['session_job'] = job

    message = (
        f'Hello {user}, I am a bot. Please let me help with your training!\n'
        'Sessão iniciada. Você pode usar comandos como /set.\n'
        'Para encerrar: /end ou aguarde 60 minutos de inatividade.'
    )

    await context.bot.send_message(chat_id=chat_id, text=message)


async def end(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    chat_data = context.chat_data

    if not chat_data.get('session_active', False):
        await context.bot.send_message(
            chat_id=chat_id, text='Nenhuma sessão ativa para encerrar.'
        )
        return

    # Close session
    chat_data['session_active'] = False
    chat_data['last_activity'] = datetime.utcnow().isoformat()

    # Cancel timeout job
    prev_job = chat_data.get('session_job')
    if prev_job:
        try:
            prev_job.schedule_removal()
        except Exception:
            pass

    await context.bot.send_message(
        chat_id=chat_id, text='Sessão encerrada manualmente.'
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
            if save_workout(
                exercise_name, reps, weight, load, update.effective_user.id
            ):
                # TODO: save this in a database with date and user_id
                message = (
                    f'Successfully registered:\n'
                    f'{exercise_name}\n'
                    f'{reps} reps - {weight}kg\n'
                    f'Load - {load}'
                )
            else:
                message = 'Error with database'

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
    This function returns today stats, broken down by set and total of the workout.
    """
    pass


async def stats_by_day(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    This function returns the stats of the day, broken down by set and total of the workout.
    """
    pass


async def report_status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    This function save your daily status.
    It's an open field. It is possible to report pain, how you slept, how you ate, etc.
    """
    pass


# Function echo - reply same text if its not a command
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text=update.message.text
    )


async def _session_timeout(context: ContextTypes.DEFAULT_TYPE):
    """
    Job callback to close the session after timeout.
    """
    job = context.job
    chat_id = job.chat_id
    chat_data = context.application.chat_data.get(chat_id, {})

    # If session is already inactive, do nothing
    if not chat_data.get('session_active'):
        return

    # Mark session closed
    chat_data['session_active'] = False
    chat_data['last_activity'] = datetime.utcnow().isoformat()

    # Send closure message
    try:
        await context.bot.send_message(
            chat_id=chat_id,
            text='Sessão encerrada por 60 minutos de inatividade.',
        )
    except Exception as e:
        logger.error(f'Erro ao enviar mensagem de timeout: {e}')


async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handle any text message: refresh session if active, echo if active, else prompt to start.
    """
    chat_id = update.effective_chat.id
    chat_data = context.chat_data

    if not chat_data.get('session_active', False):
        await context.bot.send_message(
            chat_id=chat_id,
            text='Nenhuma sessão ativa. Use /start para iniciar.',
        )
        return

    # Refresh session
    chat_data['last_activity'] = datetime.utcnow().isoformat()

    # Cancel previous timeout job
    prev_job = chat_data.get('session_job')
    if prev_job:
        try:
            prev_job.schedule_removal()
        except Exception:
            pass

    # Schedule new timeout
    job = context.application.job_queue.run_once(
        _session_timeout, when=timedelta(minutes=60), chat_id=chat_id
    )
    chat_data['session_job'] = job

    # Echo the message
    if update.message and update.message.text:
        await context.bot.send_message(
            chat_id=chat_id, text=update.message.text
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
    echo_handler = MessageHandler(
        filters.TEXT & (~filters.COMMAND), message_handler
    )
    set_handler = CommandHandler('set', set_register)
    start_handler = CommandHandler('start', start)
    end_handler = CommandHandler('end', end)

    application.add_handler(echo_handler)
    application.add_handler(set_handler)
    application.add_handler(start_handler)
    application.add_handler(end_handler)

    # Start app until killed
    application.run_polling()


if __name__ == '__main__':
    main()
