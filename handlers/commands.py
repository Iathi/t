"""
The code updates the menu_command function to use dynamic menu texts from MENU_TEXTS.
"""
import logging
from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode

from config import MESSAGES
try:
    from menus.support_menu_dynamic import get_main_menu, MENU_TEXTS
except ImportError:
    from menus.support_menu import get_main_menu
    MENU_TEXTS = {
        "main_menu": {"title": "🔧 Menu de Suporte", "description": "Selecione uma opção:"}
    }

logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler para o comando /start"""
    user = update.effective_user
    logger.info(f"Usuário {user.id} ({user.username}) iniciou o bot")

    # Enviar mensagem de boas-vindas com menu principal
    await update.message.reply_text(
        MESSAGES["welcome"],
        parse_mode="Markdown",
        reply_markup=get_main_menu()
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler para o comando /help"""
    user = update.effective_user
    logger.info(f"Usuário {user.id} ({user.username}) solicitou ajuda")

    await update.message.reply_text(
        MESSAGES["help"],
        parse_mode=ParseMode.MARKDOWN
    )

async def menu_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Mostrar menu de opções"""
    menu_text = f"*{MENU_TEXTS['main_menu']['title']}*\n\n{MENU_TEXTS['main_menu']['description']}"

    await update.message.reply_text(
        menu_text,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=get_main_menu()
    )