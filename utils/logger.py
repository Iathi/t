"""
Configuração de logging para o bot de suporte
"""

import logging
import os
from datetime import datetime
from config import LOG_LEVEL, LOG_FILE

def setup_logger():
    """Configura o sistema de logging do bot"""
    
    # Criar diretório de logs se não existir
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # Configurar formatação das mensagens de log
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    date_format = '%Y-%m-%d %H:%M:%S'
    
    # Configurar logging básico
    logging.basicConfig(
        level=getattr(logging, LOG_LEVEL.upper()),
        format=log_format,
        datefmt=date_format,
        handlers=[
            logging.FileHandler(os.path.join(log_dir, LOG_FILE), encoding='utf-8'),
            logging.StreamHandler()  # Para mostrar logs no console também
        ]
    )
    
    # Configurar logger específico para interações de suporte
    support_logger = logging.getLogger('support_interactions')
    support_handler = logging.FileHandler(
        os.path.join(log_dir, 'support_interactions.log'), 
        encoding='utf-8'
    )
    support_handler.setFormatter(logging.Formatter(log_format, date_format))
    support_logger.addHandler(support_handler)
    support_logger.setLevel(logging.INFO)
    
    # Reduzir verbosidade de bibliotecas externas
    logging.getLogger('httpx').setLevel(logging.WARNING)
    logging.getLogger('telegram').setLevel(logging.WARNING)

def log_support_interaction(user_id, username, action, details=""):
    """Log específico para interações de suporte"""
    support_logger = logging.getLogger('support_interactions')
    support_logger.info(f"User:{user_id}({username}) - Action:{action} - Details:{details}")

def log_faq_search(user_id, username, query, results_count):
    """Log específico para buscas na FAQ"""
    support_logger = logging.getLogger('support_interactions')
    support_logger.info(f"FAQ_SEARCH - User:{user_id}({username}) - Query:'{query}' - Results:{results_count}")

def log_ticket_creation(user_id, username, ticket_id, category=""):
    """Log específico para criação de tickets"""
    support_logger = logging.getLogger('support_interactions')
    support_logger.info(f"TICKET_CREATED - User:{user_id}({username}) - Ticket:{ticket_id} - Category:{category}")
