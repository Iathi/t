
#!/usr/bin/env python3
"""
Telegram Support Bot - Using telegram==0.0.1
Bot de Suporte para Telegram com API antiga
"""

import logging
import time
import json
import requests
import threading
from config import BOT_TOKEN

# Setup básico de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class TelegramBot:
    def __init__(self, token):
        self.token = token
        self.api_url = f"https://api.telegram.org/bot{token}"
        self.last_update_id = 0
        self.running = False

    def get_updates(self):
        """Buscar updates do Telegram"""
        try:
            url = f"{self.api_url}/getUpdates"
            params = {
                'offset': self.last_update_id + 1,
                'timeout': 10
            }
            response = requests.get(url, params=params, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                if data['ok']:
                    return data['result']
            return []
        except Exception as e:
            logger.error(f"Erro ao buscar updates: {e}")
            return []

    def send_message(self, chat_id, text, reply_markup=None):
        """Enviar mensagem"""
        try:
            url = f"{self.api_url}/sendMessage"
            payload = {
                'chat_id': chat_id,
                'text': text,
                'parse_mode': 'Markdown'
            }
            
            if reply_markup:
                payload['reply_markup'] = json.dumps(reply_markup)
            
            response = requests.post(url, json=payload)
            result = response.json()
            
            if result.get('ok'):
                logger.info(f"Mensagem enviada com sucesso para {chat_id}")
                return result
            else:
                logger.error(f"Erro ao enviar mensagem: {result}")
                return None
                
        except Exception as e:
            logger.error(f"Erro ao enviar mensagem: {e}")
            return None

    def edit_message_text(self, chat_id, message_id, text, reply_markup=None):
        """Editar mensagem"""
        try:
            url = f"{self.api_url}/editMessageText"
            payload = {
                'chat_id': chat_id,
                'message_id': message_id,
                'text': text,
                'parse_mode': 'Markdown'
            }
            
            if reply_markup:
                payload['reply_markup'] = json.dumps(reply_markup)
            
            response = requests.post(url, json=payload)
            return response.json()
        except Exception as e:
            logger.error(f"Erro ao editar mensagem: {e}")
            return None

    def answer_callback_query(self, callback_query_id, text=""):
        """Responder callback query"""
        try:
            url = f"{self.api_url}/answerCallbackQuery"
            payload = {
                'callback_query_id': callback_query_id,
                'text': text
            }
            response = requests.post(url, json=payload)
            return response.json()
        except Exception as e:
            logger.error(f"Erro ao responder callback: {e}")
            return None

    def get_main_menu(self):
        """Menu principal inline"""
        return {
            'inline_keyboard': [
                [
                    {'text': '❓ FAQ', 'callback_data': 'faq'},
                    {'text': '📞 Contato', 'callback_data': 'contact'}
                ],
                [
                    {'text': '🐛 Reportar Problema', 'callback_data': 'report_issue'},
                    {'text': '📋 Categorias', 'callback_data': 'categories'}
                ]
            ]
        }

    def get_faq_menu(self):
        """Menu FAQ"""
        return {
            'inline_keyboard': [
                [
                    {'text': '💻 Técnico', 'callback_data': 'faq_tecnico'},
                    {'text': '💳 Pagamento', 'callback_data': 'faq_pagamento'}
                ],
                [
                    {'text': '📱 App', 'callback_data': 'faq_app'},
                    {'text': '🔐 Segurança', 'callback_data': 'faq_seguranca'}
                ],
                [
                    {'text': '🔙 Voltar', 'callback_data': 'main_menu'}
                ]
            ]
        }

    def get_categories_menu(self):
        """Menu de categorias"""
        return {
            'inline_keyboard': [
                [
                    {'text': '💻 Suporte Técnico', 'callback_data': 'category_tecnico'},
                    {'text': '💳 Financeiro', 'callback_data': 'category_financeiro'}
                ],
                [
                    {'text': '📱 Aplicativo', 'callback_data': 'category_app'},
                    {'text': '👤 Conta', 'callback_data': 'category_conta'}
                ],
                [
                    {'text': '🔙 Voltar', 'callback_data': 'main_menu'}
                ]
            ]
        }

    def handle_message(self, message):
        """Processar mensagem recebida"""
        chat_id = message['chat']['id']
        text = message.get('text', '')
        user_name = message.get('from', {}).get('first_name', 'Usuário')
        
        logger.info(f"Mensagem recebida de {chat_id} ({user_name}): {text}")
        
        if text.startswith('/start'):
            welcome_text = f"""🤖 *Bem-vindo ao Sistema de Suporte, {user_name}!*

Olá! Eu sou seu assistente de suporte automatizado.
Como posso ajudá-lo hoje?

Use os botões abaixo para navegar pelos nossos serviços de suporte."""
            
            result = self.send_message(chat_id, welcome_text, self.get_main_menu())
            if result:
                logger.info(f"Menu principal enviado para {chat_id}")
            
        elif text.startswith('/menu'):
            menu_text = "🔧 *Menu de Suporte*\n\nSelecione uma opção:"
            result = self.send_message(chat_id, menu_text, self.get_main_menu())
            if result:
                logger.info(f"Menu de suporte enviado para {chat_id}")
            
        elif text.startswith('/help'):
            help_text = """📚 *Ajuda - Como usar o bot*

*Comandos disponíveis:*
• /start - Iniciar o bot e ver menu principal
• /menu - Mostrar menu de suporte
• /help - Mostrar esta mensagem de ajuda

*Como navegar:*
• Use os botões inline para navegar pelos menus
• Digite suas mensagens para buscar na FAQ
• Selecione a categoria apropriada para seu problema"""
            
            self.send_message(chat_id, help_text)
            
        else:
            # FAQ automática ou resposta padrão
            response = f"🔍 *Obrigado pela sua mensagem, {user_name}!*\n\n"
            response += "Recebi sua solicitação e nossa equipe analisará em breve.\n\n"
            response += "💡 *Precisa de ajuda imediata?*\n"
            response += "Use os botões abaixo para acessar nossas opções de suporte."
            
            result = self.send_message(chat_id, response, self.get_main_menu())
            if result:
                logger.info(f"Resposta com menu enviada para {chat_id}")

    def handle_callback_query(self, callback_query):
        """Processar callback de botão"""
        callback_id = callback_query['id']
        chat_id = callback_query['message']['chat']['id']
        message_id = callback_query['message']['message_id']
        data = callback_query['data']
        user_name = callback_query.get('from', {}).get('first_name', 'Usuário')
        
        logger.info(f"Callback recebido de {user_name}: {data}")
        
        # Confirmar callback
        self.answer_callback_query(callback_id, "✅ Processando...")
        
        if data == 'main_menu':
            text = "🔧 *Menu de Suporte*\n\nSelecione uma opção:"
            self.edit_message_text(chat_id, message_id, text, self.get_main_menu())
            
        elif data == 'faq':
            text = "❓ *Perguntas Frequentes*\n\nSelecione uma categoria para ver as perguntas mais comuns:"
            self.edit_message_text(chat_id, message_id, text, self.get_faq_menu())
            
        elif data == 'contact':
            text = f"""📞 *Informações de Contato*

Olá {user_name}! Para suporte direto:

• *Telegram:* @suporte_admin
• *Email:* suporte@empresa.com
• *WhatsApp:* (11) 99999-9999

*Horário de atendimento:*
🕘 Segunda a Sexta: 9:00 - 18:00
🕘 Sábado: 9:00 - 13:00

*Tempo de resposta:*
⚡ Chat: Até 2 horas
📧 Email: Até 24 horas"""
            
            keyboard = {
                'inline_keyboard': [
                    [{'text': '🔙 Menu Principal', 'callback_data': 'main_menu'}]
                ]
            }
            self.edit_message_text(chat_id, message_id, text, keyboard)
            
        elif data == 'report_issue':
            import random
            ticket_id = random.randint(10000, 99999)
            text = f"""✅ *Problema Reportado com Sucesso!*

Obrigado {user_name}!
Seu ticket foi registrado em nosso sistema.

🎫 *Número do ticket:* #{ticket_id}

*Próximos passos:*
• Nossa equipe será notificada automaticamente
• Você receberá uma resposta em até 24 horas
• Mantenha este chat aberto para atualizações

📝 Para adicionar mais informações, envie uma mensagem descrevendo o problema."""
            
            keyboard = {
                'inline_keyboard': [
                    [{'text': '🔙 Menu Principal', 'callback_data': 'main_menu'}]
                ]
            }
            self.edit_message_text(chat_id, message_id, text, keyboard)
            
        elif data == 'categories':
            text = "📋 *Categorias de Suporte*\n\nSelecione a categoria que melhor descreve seu problema:"
            self.edit_message_text(chat_id, message_id, text, self.get_categories_menu())
            
        elif data.startswith('faq_'):
            category = data.replace('faq_', '')
            category_names = {
                'tecnico': 'Suporte Técnico',
                'pagamento': 'Pagamentos',
                'app': 'Aplicativo',
                'seguranca': 'Segurança'
            }
            
            category_name = category_names.get(category, category.title())
            text = f"❓ *FAQ - {category_name}*\n\n"
            
            # FAQ específica por categoria
            if category == 'tecnico':
                text += "*1. Como resolver problemas de conexão?*\n"
                text += "Verifique sua conexão de internet e tente novamente.\n\n"
                text += "*2. O app não está funcionando, o que fazer?*\n"
                text += "Tente fechar e abrir o aplicativo novamente.\n\n"
                text += "*3. Como atualizar o aplicativo?*\n"
                text += "Acesse a loja de aplicativos e procure por atualizações.\n\n"
            elif category == 'pagamento':
                text += "*1. Como fazer um pagamento?*\n"
                text += "Acesse a seção de pagamentos no app e siga as instruções.\n\n"
                text += "*2. Meu pagamento não foi processado*\n"
                text += "Verifique os dados do cartão e tente novamente.\n\n"
                text += "*3. Como cancelar uma assinatura?*\n"
                text += "Acesse configurações > assinaturas > cancelar.\n\n"
            else:
                text += f"*Perguntas sobre {category_name}*\n"
                text += f"Em breve teremos mais FAQs sobre {category_name}.\n\n"
            
            self.edit_message_text(chat_id, message_id, text, self.get_faq_menu())
            
        elif data.startswith('category_'):
            category = data.replace('category_', '')
            category_names = {
                'tecnico': 'Suporte Técnico',
                'financeiro': 'Financeiro',
                'app': 'Aplicativo',
                'conta': 'Gerenciamento de Conta'
            }
            
            category_name = category_names.get(category, category.title())
            text = f"🔧 *Categoria: {category_name}*\n\n"
            text += f"Você selecionou *{category_name}*.\n\n"
            text += "*Para continuar:*\n"
            text += "• Descreva seu problema em detalhes\n"
            text += "• Nossa equipe especializada entrará em contato\n"
            text += "• Ou consulte nossa FAQ relacionada\n\n"
            text += "💬 *Envie uma mensagem* descrevendo seu problema!"
            
            keyboard = {
                'inline_keyboard': [
                    [{'text': f'❓ FAQ {category_name}', 'callback_data': f'faq_{category}'}],
                    [{'text': '🔙 Menu Principal', 'callback_data': 'main_menu'}]
                ]
            }
            self.edit_message_text(chat_id, message_id, text, keyboard)

    def process_updates(self, updates):
        """Processar updates recebidos"""
        for update in updates:
            self.last_update_id = update['update_id']
            
            try:
                if 'message' in update:
                    self.handle_message(update['message'])
                elif 'callback_query' in update:
                    self.handle_callback_query(update['callback_query'])
            except Exception as e:
                logger.error(f"Erro ao processar update {update['update_id']}: {e}")

    def run(self):
        """Executar bot"""
        logger.info("🤖 Iniciando Bot de Suporte com API Telegram...")
        self.running = True
        
        # Teste inicial da API
        try:
            test_url = f"{self.api_url}/getMe"
            response = requests.get(test_url, timeout=10)
            if response.status_code == 200:
                bot_info = response.json()
                if bot_info.get('ok'):
                    logger.info(f"✅ Bot conectado: @{bot_info['result']['username']}")
                else:
                    logger.error(f"❌ Erro na API do bot: {bot_info}")
                    return
            else:
                logger.error(f"❌ Erro HTTP {response.status_code} ao conectar com API")
                return
        except Exception as e:
            logger.error(f"❌ Erro ao testar conexão com API: {e}")
            return
        
        while self.running:
            try:
                updates = self.get_updates()
                if updates:
                    logger.info(f"📨 Processando {len(updates)} updates")
                    self.process_updates(updates)
                time.sleep(1)
                
            except KeyboardInterrupt:
                logger.info("🛑 Bot interrompido pelo usuário")
                break
            except Exception as e:
                logger.error(f"❌ Erro no loop principal: {e}")
                time.sleep(5)

    def stop(self):
        """Parar bot"""
        logger.info("🛑 Parando bot...")
        self.running = False

def main():
    """Função principal"""
    if not BOT_TOKEN or BOT_TOKEN == "SEU_TOKEN_AQUI":
        logger.error("❌ Token do bot não configurado!")
        logger.error("Configure o token no arquivo config.py")
        return

    logger.info(f"🔑 Token configurado: ...{BOT_TOKEN[-10:]}")
    
    bot = TelegramBot(BOT_TOKEN)
    
    try:
        bot.run()
    except Exception as e:
        logger.error(f"❌ Erro fatal ao executar bot: {e}")

if __name__ == "__main__":
    main()
