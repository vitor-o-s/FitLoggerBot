from telegram import Update, ForceReply
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters, CallbackContext
import logging
import os

# Configuração do logging para facilitar a depuração
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

logger = logging.getLogger(__name__)

# Função para iniciar a conversa
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="I'm a bot, please talk to me!"
    )
    """
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Olá {user.mention_markdown_v2()}\! Este bot vai te ajudar a registrar seus treinos\. '
        'Envie /registrar para começar\.',
        reply_markup=ForceReply(selective=True),
    )
    """

# Função para registrar treinos
def registrar(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Qual exercício você realizou?')

# Função para responder uma mensagem em CAPS
async def caps(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text_caps = ' '.join(context.args).upper()
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)

# Adiciona um manipulador para mensagens de texto
# def echo(update: Update, context: CallbackContext) -> None:
#    update.message.reply_text(update.message.text)
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)


# Função principal para executar o bot
def main() -> None:
    # Carregar o token
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    if not token:
        logger.error("Token do Telegram não encontrado. Certifique-se de que a variável de ambiente TELEGRAM_BOT_TOKEN está definida.")
        return

    # Inicializa o updater com o seu token do Bot
    
    # updater = Updater(token)

    # Obtém o dispatcher para registrar manipuladores
    # dispatcher = updater.dispatcher

    application = ApplicationBuilder().token(token).build()
    
    start_handler = CommandHandler('start', start)
    caps_handler = CommandHandler('caps', caps)
    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)

    application.add_handler(echo_handler)
    application.add_handler(caps_handler)
    application.add_handler(start_handler)
    
    # Registra os manipuladores de comandos e mensagens
    # application.add_handler(CommandHandler("start", start))
    # application.add_handler(CommandHandler("registrar", registrar))
    # application.add_handler(MessageHandler(filters.Text & ~filters.Command, echo))

    application.run_polling()


    # dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    # Inicia o Bot
    # updater.start_polling()

    # Bloqueia até que você pressione Ctrl+C ou o processo receba SIGINT, SIGTERM ou SIGABRT
    # updater.idle()

if __name__ == '__main__':
    main()
