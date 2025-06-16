"""
Configurações do Bot de Suporte
"""

import os

# Carregar variáveis do arquivo .env se existir
if os.path.exists('.env'):
    with open('.env', 'r') as f:
        for line in f:
            if line.strip() and not line.startswith('#') and '=' in line:
                key, value = line.strip().split('=', 1)
                os.environ[key] = value

# Token do bot (obtido do BotFather)
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "8067162502:AAGp2Qsr51XFIGEwGtCNOuXM0m_-9OHzTzs")

# Configurações de logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FILE = "support_bot.log"

# Configurações do suporte
SUPPORT_CONTACT = os.getenv("SUPPORT_CONTACT", "@admin")
SUPPORT_EMAIL = os.getenv("SUPPORT_EMAIL", "support@company.com")

# Mensagens do sistema
MESSAGES = {
    "welcome": """
🤖 *Bem-vindo ao Sistema de Suporte!*

Olá! Eu sou seu assistente de suporte automatizado.
Como posso ajudá-lo hoje?

Use os botões abaixo para navegar pelos nossos serviços de suporte.
""",
    
    "help": """
📚 *Ajuda - Como usar o bot*

*Comandos disponíveis:*
• /start - Iniciar o bot e ver menu principal
• /menu - Mostrar menu de suporte
• /help - Mostrar esta mensagem de ajuda

*Como navegar:*
• Use os botões inline para navegar pelos menus
• Digite suas mensagens para buscar na FAQ
• Selecione a categoria apropriada para seu problema

*Precisa de mais ajuda?*
Entre em contato com nosso suporte: {}
""".format(SUPPORT_CONTACT),
    
    "menu_title": "🔧 *Menu de Suporte*\n\nSelecione uma opção:",
    
    "contact_info": """
📞 *Informações de Contato*

Para suporte direto, entre em contato:

• *Telegram:* {}
• *Email:* {}

*Horário de atendimento:*
Segunda a Sexta: 9:00 - 18:00
Sábado: 9:00 - 13:00

*Tempo de resposta:*
• Chat: Até 2 horas
• Email: Até 24 horas
""".format(SUPPORT_CONTACT, SUPPORT_EMAIL),

    "issue_reported": """
✅ *Problema Reportado*

Obrigado por reportar o problema!
Seu ticket foi registrado em nosso sistema.

*Próximos passos:*
• Nossa equipe será notificada
• Você receberá uma resposta em até 24 horas
• Mantenha este chat aberto para atualizações

*Número do ticket:* #{ticket_id}
""",

    "no_faq_found": """
❌ *Nenhuma FAQ encontrada*

Desculpe, não encontrei informações sobre sua consulta.

*O que você pode fazer:*
• Tente palavras-chave diferentes
• Navegue pelas categorias do menu
• Entre em contato com nosso suporte

Use /menu para voltar ao menu principal.
"""
}
