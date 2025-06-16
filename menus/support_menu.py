"""
Menus e teclados inline para o sistema de suporte
"""

from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def get_main_menu():
    """Retorna o menu principal do sistema de suporte"""
    keyboard = [
        [
            InlineKeyboardButton("❓ FAQ", callback_data="faq"),
            InlineKeyboardButton("📞 Contato", callback_data="contact")
        ],
        [
            InlineKeyboardButton("🐛 Reportar Problema", callback_data="report_issue"),
            InlineKeyboardButton("📋 Categorias", callback_data="categories")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_faq_menu():
    """Retorna o menu de FAQ com categorias"""
    keyboard = [
        [
            InlineKeyboardButton("💻 Técnico", callback_data="faq_tecnico"),
            InlineKeyboardButton("💳 Pagamento", callback_data="faq_pagamento")
        ],
        [
            InlineKeyboardButton("👤 Conta", callback_data="faq_conta"),
            InlineKeyboardButton("📱 App", callback_data="faq_app")
        ],
        [
            InlineKeyboardButton("🔐 Segurança", callback_data="faq_seguranca"),
            InlineKeyboardButton("📋 Geral", callback_data="faq_geral")
        ],
        [
            InlineKeyboardButton("🔙 Voltar", callback_data="main_menu")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_categories_menu():
    """Retorna o menu de categorias de suporte"""
    keyboard = [
        [
            InlineKeyboardButton("💻 Problemas Técnicos", callback_data="category_problemas_tecnicos"),
            InlineKeyboardButton("💳 Questões de Pagamento", callback_data="category_questoes_pagamento")
        ],
        [
            InlineKeyboardButton("👤 Gerenciamento de Conta", callback_data="category_gerenciamento_conta"),
            InlineKeyboardButton("📱 Problemas do App", callback_data="category_problemas_app")
        ],
        [
            InlineKeyboardButton("🔐 Segurança", callback_data="category_seguranca"),
            InlineKeyboardButton("💬 Feedback", callback_data="category_feedback")
        ],
        [
            InlineKeyboardButton("🔙 Voltar", callback_data="main_menu")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_back_to_menu():
    """Retorna botão simples para voltar ao menu"""
    keyboard = [[InlineKeyboardButton("🔙 Menu Principal", callback_data="main_menu")]]
    return InlineKeyboardMarkup(keyboard)

def get_back_to_faq():
    """Retorna botão para voltar ao menu FAQ"""
    keyboard = [
        [
            InlineKeyboardButton("🔙 FAQ", callback_data="faq"),
            InlineKeyboardButton("🏠 Menu Principal", callback_data="main_menu")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)
