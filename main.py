
#!/usr/bin/env python3
"""
Telegram Support Bot - Main Entry Point
Ponto de entrada principal que inicia bot e painel web
"""

import os
import sys
import time
import threading
import logging
import asyncio
import signal
import psutil
from pathlib import Path

# Adicionar o diretório atual ao path do Python
sys.path.insert(0, str(Path(__file__).parent))

def setup_logging():
    """Configurar logging básico"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler('support_bot.log')
        ]
    )

def kill_existing_bot_processes():
    """Mata processos existentes do bot para evitar conflitos"""
    try:
        current_pid = os.getpid()
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                if proc.info['pid'] == current_pid:
                    continue
                    
                cmdline = proc.info['cmdline']
                if cmdline and any('bot.py' in cmd or 'main.py' in cmd for cmd in cmdline):
                    if any('python' in cmd for cmd in cmdline):
                        logging.info(f"Matando processo existente do bot: PID {proc.info['pid']}")
                        proc.terminate()
                        proc.wait(timeout=5)
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.TimeoutExpired):
                pass
    except Exception as e:
        logging.warning(f"Erro ao verificar processos existentes: {e}")

def start_web_panel():
    """Iniciar painel web"""
    try:
        import socket
        
        # Verificar se a porta está disponível
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex(('127.0.0.1', 5000))
        sock.close()
        
        if result == 0:
            logging.warning("Porta 5000 já em uso, tentando liberar...")
            os.system("fuser -k 5000/tcp 2>/dev/null")
            time.sleep(2)
        
        from web_panel import app
        app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)
    except Exception as e:
        logging.error(f"Erro ao iniciar painel web: {e}")

def start_bot():
    """Iniciar bot do Telegram"""
    try:
        # Aguardar um pouco para garantir que processos antigos foram terminados
        time.sleep(3)
        
        # Verificar se há token configurado
        from config import BOT_TOKEN
        if not BOT_TOKEN or BOT_TOKEN == "SEU_TOKEN_AQUI":
            logging.error("❌ Token do bot não configurado! Configure o token no painel web.")
            return
        
        logging.info("🤖 Iniciando bot após verificação de conflitos...")
        from bot import main as bot_main

        bot_main()

        asyncio.run(bot_main())

        
    except Exception as e:
        logging.error(f"Erro ao iniciar bot: {e}")
        # Tentar uma vez mais após delay
        time.sleep(10)
        try:
            logging.info("🔄 Tentando reiniciar o bot...")
            from bot import main as bot_main_retry
            asyncio.run(bot_main_retry())
        except Exception as e2:
            logging.error(f"Falha ao reiniciar bot: {e2}")

def signal_handler(signum, frame):
    """Handler para sinais de sistema"""
    logging.info("🛑 Recebido sinal de parada, encerrando sistema...")
    sys.exit(0)

def main():
    """Função principal"""
    setup_logging()
    logger = logging.getLogger(__name__)
    
    # Configurar handlers de sinal
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    logger.info("🚀 Iniciando Sistema de Suporte Telegram...")
    
    # Matar processos existentes do bot para evitar conflitos
    kill_existing_bot_processes()
    time.sleep(2)
    
    # Iniciar painel web em thread principal
    web_thread = threading.Thread(target=start_web_panel, daemon=False)
    web_thread.start()
    
    # Iniciar bot em thread separada
    bot_thread = threading.Thread(target=start_bot, daemon=True)
    bot_thread.start()
    
    logger.info("✅ Sistema iniciado com sucesso!")
    logger.info("🌐 Painel web: http://0.0.0.0:5000")
    logger.info("⏹️ Pressione Ctrl+C para parar")
    
    try:
        web_thread.join()
    except KeyboardInterrupt:
        logger.info("🛑 Sistema sendo encerrado...")

if __name__ == "__main__":
    main()
