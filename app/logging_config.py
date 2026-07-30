import logging
import sys
from flask import Flask

def setup_logging(app: Flask):
    """
    Configure application-wide logging for Flask and Python logging.
    """
    log_level = logging.DEBUG if app.config.get('DEBUG') else logging.INFO
    
    # Define a clean, uniform format
    log_format = logging.Formatter(
        '[%(asctime)s] %(levelname)s in %(name)s: %(message)s'
    )
    
    # Configure root logger handler
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(log_format)
    handler.setLevel(log_level)
    
    # Clear default Flask handlers to avoid duplicated logs
    app.logger.handlers.clear()
    app.logger.addHandler(handler)
    app.logger.setLevel(log_level)
    
    # Configure top-level app logger
    module_logger = logging.getLogger('app')
    module_logger.handlers.clear()
    module_logger.addHandler(handler)
    module_logger.setLevel(log_level)
    
    app.logger.info(f"Logging initialized. Level: {logging.getLevelName(log_level)}")
