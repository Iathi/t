import os
import json
from pathlib import Path

# Token do bot - Configure através do painel web ou diretamente aqui
BOT_TOKEN = os.getenv("BOT_TOKEN", "8060615315:AAGZbcQyeyAvrecOEM_lyMjfvmOO-eLnedY")

# Configurações de logging
LOG_LEVEL = "INFO"
LOG_FILE = "support_bot.log"

# Configurações do bot
BOT_USERNAME = os.getenv("BOT_USERNAME", "")
WEBHOOK_URL = os.getenv("WEBHOOK_URL", "")

# Configurações do painel web
FLASK_SECRET_KEY = os.getenv("FLASK_SECRET_KEY", "dev-secret-key-change-in-production")

# Configuração do painel
PANEL_CONFIG_FILE = "panel_config.json"

def load_panel_config():
    """Carrega configurações do painel"""
    if Path(PANEL_CONFIG_FILE).exists():
        try:
            with open(PANEL_CONFIG_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Erro ao carregar config: {e}")

    # Configuração padrão
    return {
        "bot_settings": {
            "welcome_message": """🤖 *Bem-vindo ao Sistema de Suporte!*

Olá! Eu sou seu assistente de suporte automatizado.
Como posso ajudá-lo hoje?

Use os botões abaixo para navegar pelos nossos serviços de suporte.""",
            "support_contact": "@Webprontos",
            "support_email": "suporte@empresa.com",
            "auto_reply": True,
            "bot_name": "Bot de Suporte",
            "log_level": "INFO"
        },
        "menu_settings": {
            "show_faq": True,
            "show_contact": True,
            "show_categories": True,
            "custom_buttons": []
        }
    }

def save_panel_config(config):
    """Salva configurações do painel"""
    try:
        with open(PANEL_CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Erro ao salvar config: {e}")
        return False

# Carregar configurações
try:
    PANEL_CONFIG = load_panel_config()
except Exception as e:
    print(f"Erro ao inicializar config: {e}")
    PANEL_CONFIG = {
        "bot_settings": {
            "welcome_message": """🤖 *Bem-vindo ao Sistema de Suporte Webpronto Automação!*

Olá! Eu sou seu assistente de suporte automatizado.
Como posso ajudá-lo hoje?

Use os botões abaixo para navegar pelos nossos serviços de suporte.""",
            "support_contact": "@WebPronto",
            "support_email": "suporte@empresa.com",
            "auto_reply": True,
            "bot_name": "Bot de Suporte",
            "log_level": "INFO"
        },
        "menu_settings": {
            "show_faq": True,
            "show_contact": True,
            "show_categories": True,
            "custom_buttons": []
        }
    }

# Mensagens do sistema
def get_safe_config_value(config, keys, default=""):
    """Obter valor da configuração de forma segura"""
    try:
        value = config
        for key in keys:
            value = value[key]
        return value
    except (KeyError, TypeError):
        return default

MESSAGES = {
    "welcome": get_safe_config_value(PANEL_CONFIG, ["bot_settings", "welcome_message"], 
                                   """🤖 *Bem-vindo ao Sistema de Suporte Webpronto Automação!*

Olá! Eu sou seu assistente de suporte automatizado.
Como posso ajudá-lo hoje?

Use os botões abaixo para navegar pelos nossos serviços de suporte."""),
    "help": "Use os comandos /start, /menu ou /help para navegar.",
    "error": "Ocorreu um erro. Tente novamente mais tarde.",
    "contact_info": f"Contato: {get_safe_config_value(PANEL_CONFIG, ['bot_settings', 'support_contact'], '@Webprontos')}\nEmail: {get_safe_config_value(PANEL_CONFIG, ['bot_settings', 'support_email'], 'suporte@empresa.com')}"
}
