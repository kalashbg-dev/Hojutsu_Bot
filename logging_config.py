import logging
import logging.handlers
import os
from pathlib import Path

def setup_logging():
    """
    Configura el sistema de logging de forma flexible.
    Permite ajustar el nivel de log y los handlers mediante variables de entorno:
    - LOG_LEVEL: Nivel de log (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    - LOG_TO_FILE: '1' para habilitar log a archivo, '0' para deshabilitar
    - LOG_TO_CONSOLE: '1' para habilitar log a consola, '0' para deshabilitar
    """
    log_dir = Path('logs')
    log_dir.mkdir(exist_ok=True)

    logger = logging.getLogger()
    # Evitar agregar handlers múltiples veces
    if logger.hasHandlers():
        logger.handlers.clear()

    log_level = os.getenv('LOG_LEVEL', 'INFO').upper()
    logger.setLevel(getattr(logging, log_level, logging.INFO))

    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    log_to_file = os.getenv('LOG_TO_FILE', '1') == '1'
    log_to_console = os.getenv('LOG_TO_CONSOLE', '1') == '1'

    if log_to_file:
        file_handler = logging.handlers.RotatingFileHandler(
            'logs/bot.log',
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    if log_to_console:
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)

    return logger
