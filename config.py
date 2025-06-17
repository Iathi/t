import os
import json
from pathlib import Path

# Token do bot - Configure através do painel web ou diretamente aqui
BOT_TOKEN = os.getenv("BOT_TOKEN", "SEU_TOKEN_AQUI")

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
            "welcome_message": "Bem-vindo ao Sistema de Suporte!",
            "support_contact": "@admin",
            "support_email": "suporte@empresa.com",
            "auto_reply": True
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
            "welcome_message": "Bem-vindo ao Sistema de Suporte!",
            "support_contact": "@admin",
            "support_email": "suporte@empresa.com",
            "auto_reply": True
        },
        "menu_settings": {
            "show_faq": True,
            "show_contact": True,
            "show_categories": True,
            "custom_buttons": []
        }
    }

# Mensagens do sistema
MESSAGES = {
    "welcome": PANEL_CONFIG["bot_settings"]["welcome_message"],
    "help": "Use os comandos /start, /menu ou /help para navegar.",
    "error": "Ocorreu um erro. Tente novamente mais tarde.",
    "contact_info": f"Contato: {PANEL_CONFIG['bot_settings']['support_contact']}\nEmail: {PANEL_CONFIG['bot_settings']['support_email']}"
}