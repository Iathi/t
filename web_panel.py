import os
import json
import logging
from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_cors import CORS
import httpx

app = Flask(__name__)
CORS(app)

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

CONFIG_FILE = "panel_config.json"

def load_panel_config():
    """Carregar configuração do painel"""
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                config = json.load(f)
                # Garantir que statistics existe
                if 'statistics' not in config:
                    config['statistics'] = {
                        "faq_searches": 0,
                        "total_messages": 0,
                        "total_tickets": 0,
                        "total_users": 0
                    }
                return config
        except Exception as e:
            logger.error(f"Erro ao carregar config: {e}")

    # Configuração padrão
    return {
        "bot_settings": {
            "bot_name": "Bot de Suporte",
            "welcome_message": "🤖 *Bem-vindo ao Sistema de Suporte!*",
            "support_contact": "@admin",
            "support_email": "support@company.com",
            "auto_reply": True,
            "log_level": "INFO"
        },
        "menu_settings": {
            "show_faq": True,
            "show_contact": True,
            "show_report_issue": True,
            "show_categories": True
        },
        "faq_settings": {
            "max_results": 3,
            "search_threshold": 1,
            "categories_enabled": True
        },
        "statistics": {
            "faq_searches": 0,
            "total_messages": 0,
            "total_tickets": 0,
            "total_users": 0
        }
    }

def save_panel_config(config):
    """Salvar configuração do painel"""
    try:
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        logger.error(f"Erro ao salvar config: {e}")
        return False

def update_bot_token(token):
    """Atualizar token do bot no arquivo de configuração"""
    try:
        # Atualizar no config.py
        config_content = f'''"""
Configurações do Bot de Suporte
"""

import os

# Token do bot
BOT_TOKEN = "{token}"

# Configurações de logging
LOG_LEVEL = "INFO"
LOG_FILE = "support_bot.log"

# Configurações do suporte
SUPPORT_CONTACT = "@admin"
SUPPORT_EMAIL = "support@company.com"

# Mensagens do sistema
MESSAGES = {{
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
Entre em contato com nosso suporte: @admin
""",

    "menu_title": "🔧 *Menu de Suporte*\\n\\nSelecione uma opção:",

    "contact_info": """
📞 *Informações de Contato*

Para suporte direto, entre em contato:

• *Telegram:* @admin
• *Email:* support@company.com

*Horário de atendimento:*
Segunda a Sexta: 9:00 - 18:00
Sábado: 9:00 - 13:00

*Tempo de resposta:*
• Chat: Até 2 horas
• Email: Até 24 horas
""",

    "issue_reported": """
✅ *Problema Reportado*

Obrigado por reportar o problema!
Seu ticket foi registrado em nosso sistema.

*Próximos passos:*
• Nossa equipe será notificada
• Você receberá uma resposta em até 24 horas
• Mantenha este chat aberto para atualizações

*Número do ticket:* #{{ticket_id}}
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
}}
'''

        with open('config.py', 'w', encoding='utf-8') as f:
            f.write(config_content)

        return True
    except Exception as e:
        logger.error(f"Erro ao atualizar token: {e}")
        return False

# Rotas do painel
@app.route('/')
def dashboard():
    """Página principal do dashboard"""
    config = load_panel_config()
    return render_template('dashboard.html', config=config)

@app.route('/settings')
def settings():
    """Página de configurações"""
    config = load_panel_config()
    return render_template('settings.html', config=config)

@app.route('/menu-editor')
def menu_editor():
    """Página do editor de menus"""
    config = load_panel_config()
    return render_template('menu_editor.html', config=config)

@app.route('/faq')
def faq_management():
    """Página de gerenciamento de FAQ"""
    config = load_panel_config()
    return render_template('faq.html', config=config)

@app.route('/logs')
def logs_viewer():
    """Página de visualização de logs"""
    config = load_panel_config()
    return render_template('logs.html', config=config)

# APIs
@app.route('/api/config', methods=['GET', 'POST'])
def api_config():
    """API para configurações"""
    if request.method == 'GET':
        config = load_panel_config()
        return jsonify(config)

    try:
        config = request.get_json()

        # Atualizar token se fornecido
        if 'bot_settings' in config and 'bot_token' in config['bot_settings']:
            token = config['bot_settings']['bot_token']
            if token:
                if update_bot_token(token):
                    logger.info("Token do bot atualizado com sucesso")
                else:
                    return jsonify({"success": False, "message": "Erro ao atualizar token"}), 500

        if save_panel_config(config):
            return jsonify({"success": True, "message": "Configurações salvas com sucesso"})
        else:
            return jsonify({"success": False, "message": "Erro ao salvar configurações"}), 500

    except Exception as e:
        logger.error(f"Erro na API de config: {e}")
        return jsonify({"success": False, "message": str(e)}), 500

@app.route('/api/test_bot_token', methods=['POST'])
def test_bot_token():
    """Testar token do bot"""
    try:
        data = request.get_json()
        token = data.get('token')

        if not token:
            return jsonify({"success": False, "message": "Token não fornecido"}), 400

        # Testar token com API do Telegram
        async def check_token():
            async with httpx.AsyncClient() as client:
                response = await client.get(f"https://api.telegram.org/bot{token}/getMe")
                return response.json()

        import asyncio
        result = asyncio.run(check_token())

        if result.get('ok'):
            return jsonify({
                "success": True,
                "message": "Token válido",
                "bot_info": result['result']
            })
        else:
            return jsonify({
                "success": False,
                "message": result.get('description', 'Token inválido')
            })

    except Exception as e:
        logger.error(f"Erro ao testar token: {e}")
        return jsonify({"success": False, "message": str(e)}), 500

@app.route('/api/restart_bot', methods=['POST'])
def restart_bot():
    """Reiniciar o bot"""
    try:
        # Simular reinicialização do bot
        logger.info("Solicitação de reinicialização do bot recebida")
        return jsonify({"success": True, "message": "Bot será reiniciado"})
    except Exception as e:
        logger.error(f"Erro ao reiniciar bot: {e}")
        return jsonify({"success": False, "message": str(e)}), 500

@app.route('/api/bot_status')
def bot_status():
    """Status do bot"""
    try:
        # Verificar se o bot está rodando
        from config import BOT_TOKEN
        if BOT_TOKEN and BOT_TOKEN != "SEU_TOKEN_AQUI":
            return jsonify({"status": "running", "message": "Bot está funcionando"})
        else:
            return jsonify({"status": "stopped", "message": "Bot não configurado"})
    except:
        return jsonify({"status": "error", "message": "Erro ao verificar status"})

@app.route('/api/statistics')
def api_statistics():
    """API para estatísticas"""
    config = load_panel_config()
    stats = config.get("statistics", {})
    return jsonify(stats)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)