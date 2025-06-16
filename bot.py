#!/usr/bin/env python3
"""
Telegram Support Bot - Main Entry Point
Bot de Suporte para Telegram com sistema de menus interativo
"""

import os
import logging
import threading
import time
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters

from config import BOT_TOKEN
from handlers.commands import start, help_command, menu_command
from handlers.callbacks import handle_callback
from handlers.messages import handle_message
from utils.logger import setup_logger



def main():
    """Função principal para inicializar e executar o bot"""
    
    # Configurar logging
    setup_logger()
    logger = logging.getLogger(__name__)
    
    # Verificar se o token está configurado
    if not BOT_TOKEN or BOT_TOKEN == "SEU_TOKEN_AQUI":
        logger.error("❌ Token do bot não configurado! Configure o token no painel web.")
        return
    
    logger.info("🤖 Iniciando Bot de Suporte...")
    
    try:
        # Criar aplicação do bot
        application = Application.builder().token(BOT_TOKEN).build()
        
        # Registrar handlers de comandos
        application.add_handler(CommandHandler("start", start))
        application.add_handler(CommandHandler("help", help_command))
        application.add_handler(CommandHandler("menu", menu_command))
        
        # Registrar handler de callbacks (botões inline)
        application.add_handler(CallbackQueryHandler(handle_callback))
        
        # Registrar handler de mensagens de texto
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
        
        logger.info("✅ Bot de Suporte iniciado com sucesso!")
        
        # Executar o bot com configurações específicas
        application.run_polling(
            allowed_updates=["message", "callback_query"],
            drop_pending_updates=True,
            close_loop=False
        )
        
    except Exception as e:
        logger.error(f"❌ Erro ao iniciar bot: {e}")
        # Tentar uma abordagem alternativa se a primeira falhar
        try:
            logger.info("🔄 Tentando inicialização alternativa...")
            application.run_polling(drop_pending_updates=True)
        except Exception as e2:
            logger.error(f"❌ Erro na inicialização alternativa: {e2}")
            raise e

if __name__ == "__main__":
    main()
