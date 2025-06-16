
"""
Handlers para mensagens de texto
"""

import logging
from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode

from config import MESSAGES
from data.faq import search_faq
try:
    from menus.support_menu_dynamic import get_main_menu
except ImportError:
    from menus.support_menu import get_main_menu

logger = logging.getLogger(__name__)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler para mensagens de texto dos usuários"""
    user = update.effective_user
    message_text = update.message.text
    
    logger.info(f"Usuário {user.id} ({user.username}) enviou: {message_text}")
    
    # Buscar na FAQ
    results = search_faq(message_text)
    
    if results:
        # Construir resposta com resultados da FAQ
        response = "🔍 *Resultados encontrados:*\n\n"
        
        for i, faq in enumerate(results[:3], 1):  # Limitar a 3 resultados
            response += f"*{i}. {faq['question']}*\n"
            response += f"{faq['answer']}\n\n"
        
        response += "💡 *Precisa de mais ajuda?*\n"
        response += "Use os botões abaixo para mais opções."
        
        await update.message.reply_text(
            response,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=get_main_menu()
        )
    else:
        # Nenhum resultado encontrado
        await update.message.reply_text(
            MESSAGES["no_faq_found"],
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=get_main_menu()
        )
    
    # Log da interação para estatísticas
    logger.info(f"FAQ_SEARCH: Usuário {user.id} buscou por '{message_text}' - {len(results)} resultados")
