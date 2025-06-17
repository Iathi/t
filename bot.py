#!/usr/bin/env python3
"""
Telegram Support Bot - Main Entry Point
Bot de Suporte para Telegram com sistema de menus interativo
"""

import logging
import asyncio

from telegram.ext import (
    Application,
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
)

from config import BOT_TOKEN
from handlers.commands import start, help_command, menu_command
from handlers.callbacks import handle_callback
from handlers.messages import handle_message
from utils.logger import setup_logger

async def main():
    """Função principal para inicializar e executar o bot"""
    setup_logger()
    logger = logging.getLogger(__name__)

    if not BOT_TOKEN or BOT_TOKEN == "SEU_TOKEN_AQUI":
        logger.error("❌ Token do bot não configurado! Configure o token no painel web.")
        return

    logger.info("🤖 Iniciando Bot de Suporte...")

    try:
        # Inicializa o bot com ApplicationBuilder
        application = (
            ApplicationBuilder()
            .token(BOT_TOKEN)
            .build()
        )

        # Comandos
        application.add_handler(CommandHandler("start", start))
        application.add_handler(CommandHandler("help", help_command))
        application.add_handler(CommandHandler("menu", menu_command))

        # Callback de botões
        application.add_handler(CallbackQueryHandler(handle_callback))

        # Mensagens de texto
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

        logger.info("✅ Bot de Suporte iniciado com sucesso!")

        # Inicia o polling (modo assíncrono)
        await application.run_polling(
            allowed_updates=["message", "callback_query"],
            drop_pending_updates=True
        )

    except Exception as e:
        logger.exception(f"❌ Erro ao iniciar o bot: {e}")

if __name__ == "__main__":
    asyncio.run(main())
