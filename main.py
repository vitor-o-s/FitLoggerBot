from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import logging

# Configuração do logging para facilitar a depuração
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Função para iniciar a conversa
def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Olá {user.mention_markdown_v2()}\! Este bot vai te ajudar a registrar seus treinos\. '
        'Envie /registrar para começar\.',
        reply_markup=ForceReply(selective=True),
    )

# Função para registrar treinos
def registrar(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Qual exercício você realizou?')

# Adiciona um manipulador para mensagens de texto
def echo(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(update.message.text)

# Função principal para executar o bot
def main() -> None:
    # Inicializa o updater com o seu token do Bot
    updater = Updater("SEU_TOKEN_AQUI")

    # Obtém o dispatcher para registrar manipuladores
    dispatcher = updater.dispatcher

    # Registra os manipuladores de comandos e mensagens
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("registrar", registrar))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    # Inicia o Bot
    updater.start_polling()

    # Bloqueia até que você pressione Ctrl+C ou o processo receba SIGINT, SIGTERM ou SIGABRT
    updater.idle()

if __name__ == '__main__':
    main()
