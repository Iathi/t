
"""
Menus e teclados inline para o sistema de suporte - GERADO AUTOMATICAMENTE
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
            InlineKeyboardButton("🔧 Reportar Problema", callback_data="report_issue"),
            InlineKeyboardButton("📋 Categorias", callback_data="categories")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_faq_menu():
    """Retorna o menu de FAQ com categorias"""
    keyboard = [
        [
            InlineKeyboardButton("💻 Técnico", callback_data="faq_tecnico"),
            InlineKeyboardButton("📋 Conta", callback_data="faq_conta")
        ],
        [
            InlineKeyboardButton("💰 Pagamento", callback_data="faq_pagamento"),
            InlineKeyboardButton("📦 Produtos", callback_data="faq_produtos")
        ],
        [InlineKeyboardButton("🔙 Voltar", callback_data="main_menu")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_categories_menu():
    """Retorna o menu de categorias de suporte"""
    keyboard = [
        [
            InlineKeyboardButton("🔧 Suporte Técnico", callback_data="category_suporte_tecnico"),
            InlineKeyboardButton("💰 Financeiro", callback_data="category_financeiro")
        ],
        [
            InlineKeyboardButton("📦 Produtos", callback_data="category_produtos"),
            InlineKeyboardButton("👤 Conta", callback_data="category_conta")
        ],
        [InlineKeyboardButton("🔙 Voltar", callback_data="main_menu")]
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

# Configuração dos títulos e descrições dos menus
MENU_TEXTS = {
    "main_menu": {
        "title": "🔧 Menu de Suporte",
        "description": "Selecione uma opção:"
    },
    "faq_menu": {
        "title": "❓ Perguntas Frequentes",
        "description": "Selecione uma categoria:"
    },
    "categories_menu": {
        "title": "📋 Categorias de Suporte",
        "description": "Selecione a categoria:"
    }
}
