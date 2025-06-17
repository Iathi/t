"""
Handlers para callbacks de botões inline
"""

import logging
from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode

from config import MESSAGES
try:
    from menus.support_menu_dynamic import get_main_menu, get_faq_menu, get_categories_menu, get_back_to_faq, MENU_TEXTS
    USE_DYNAMIC_MENU = True
except ImportError:
    from menus.support_menu import get_main_menu, get_faq_menu, get_categories_menu
    USE_DYNAMIC_MENU = False
    MENU_TEXTS = {
        "main_menu": {"title": "🔧 Menu de Suporte", "description": "Selecione uma opção:"},
        "faq_menu": {"title": "❓ Perguntas Frequentes", "description": "Selecione uma categoria:"},
        "categories_menu": {"title": "📋 Categorias de Suporte", "description": "Selecione a categoria:"}
    }
from data.faq import search_faq, get_faq_by_category

logger = logging.getLogger(__name__)

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler principal para callbacks de botões inline"""
    query = update.callback_query
    user = update.effective_user
    data = query.data

    logger.info(f"Usuário {user.id} ({user.username}) clicou em: {data}")

    # Confirmar o callback
    await query.answer()

    try:
        if data == "main_menu":
            await show_main_menu(query)
        elif data == "faq":
            await show_faq_menu(query)
        elif data == "contact":
            await show_contact_info(query)
        elif data == "report_issue":
            await show_report_issue(query)
        elif data == "categories":
            await show_categories_menu(query)
        elif data.startswith("faq_"):
            await show_faq_category(query, data)
        elif data.startswith("category_"):
            await show_category_support(query, data)
        else:
            logger.warning(f"Callback não reconhecido: {data}")
            await query.edit_message_text("❌ Opção não reconhecida. Use /menu para voltar ao início.")

    except Exception as e:
        logger.error(f"Erro ao processar callback {data}: {e}")
        await query.edit_message_text("❌ Ocorreu um erro. Tente novamente ou use /menu.")

async def show_main_menu(query):
    """Mostrar menu principal"""
    await query.edit_message_text(
        MESSAGES["menu_title"],
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=get_main_menu()
    )

async def show_faq_menu(query):
    """Mostrar menu de FAQ"""
    text = """
❓ *Perguntas Frequentes*

Selecione uma categoria para ver as perguntas mais comuns:
"""
    await query.edit_message_text(
        text,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=get_faq_menu()
    )

async def show_contact_info(query):
    """Mostrar informações de contato"""
    from datetime import datetime
    
    # Enviar alerta para @Webprontos
    user = query.from_user
    alert_text = f"""🚨 *ALERTA DE CONTATO*

Um usuário solicitou informações de contato:

👤 *Usuário:* {user.first_name or 'N/A'} {user.last_name or ''}
🆔 *ID:* `{user.id}`
📱 *Username:* @{user.username or 'N/A'}
⏰ *Horário:* {datetime.now().strftime('%d/%m/%Y às %H:%M:%S')}

💬 *Ação:* Usuário clicou no botão "Contato"

Considere entrar em contato com este usuário para oferecer suporte personalizado."""
    
    try:
        # Enviar para @Webprontos
        await query.bot.send_message(
            chat_id="@Webprontos",
            text=alert_text,
            parse_mode=ParseMode.MARKDOWN
        )
        logger.info(f"Alerta de contato enviado para @Webprontos - Usuário: {user.first_name} ({user.id})")
    except Exception as e:
        logger.error(f"Erro ao enviar alerta de contato: {e}")
    
    # Mostrar informações de contato com confirmação
    contact_text = MESSAGES["contact_info"] + "\n\n✅ *Nossa equipe foi notificada sobre seu interesse em contato!*"
    
    await query.edit_message_text(
        contact_text,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=get_main_menu()
    )

async def show_report_issue(query):
    """Mostrar formulário de reporte de problema"""
    import random
    ticket_id = random.randint(1000, 9999)

    message = MESSAGES["issue_reported"].format(ticket_id=ticket_id)

    await query.edit_message_text(
        message,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=get_main_menu()
    )

    logger.info(f"Ticket #{ticket_id} criado para usuário {query.from_user.id}")

async def show_categories_menu(query):
    """Mostrar menu de categorias de suporte"""
    text = """
📋 *Categorias de Suporte*

Selecione a categoria que melhor descreve seu problema:
"""
    await query.edit_message_text(
        text,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=get_categories_menu()
    )

async def show_faq_category(query, data):
    """Mostrar FAQ de uma categoria específica"""
    category = data.replace("faq_", "")
    faqs = get_faq_by_category(category)

    if faqs:
        text = f"❓ *FAQ - {category.title()}*\n\n"
        for i, faq in enumerate(faqs, 1):
            text += f"*{i}. {faq['question']}*\n{faq['answer']}\n\n"
    else:
        text = f"❌ Nenhuma FAQ encontrada para a categoria: {category}"

    await query.edit_message_text(
        text,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=get_faq_menu()
    )

async def show_category_support(query, data):
    """Mostrar suporte para categoria específica"""
    category = data.replace("category_", "").replace("_", " ")

    text = f"🔧 *Suporte - {category.title()}*\n\n"
    text += f"Você selecionou a categoria: *{category}*\n\n"
    text += "Para continuar:\n"
    text += "• Descreva seu problema em detalhes\n"
    text += "• Nossa equipe entrará em contato\n"
    text += "• Ou consulte nossa FAQ relacionada\n\n"
    text += "Use os botões abaixo para mais opções."

    await query.edit_message_text(
        text,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=get_main_menu()
    )
