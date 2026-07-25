import logging
import sys
from pythonjsonlogger import jsonlogger
from typing import Optional

class CustomJsonFormatter(jsonlogger.JsonFormatter):
    """Custom JSON formatter for structured logging"""
    
    def add_fields(self, log_record, record, message_dict):
        super().add_fields(log_record, record, message_dict)
        if not log_record.get('timestamp'):
            log_record['timestamp'] = self.formatTime(record, self.datefmt)
        if not log_record.get('level'):
            log_record['level'] = record.levelname
        if not log_record.get('logger'):
            log_record['logger'] = record.name

def setup_logging(level: str = "INFO", json_format: bool = True) -> logging.Logger:
    """Setup logging configuration"""
    
    # Create logger
    logger = logging.getLogger()
    logger.setLevel(getattr(logging, level.upper()))
    
    # Remove existing handlers
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
    
    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    
    if json_format:
        # JSON formatter for production
        formatter = CustomJsonFormatter(
            '%(timestamp)s %(level)s %(name)s %(message)s',
            datefmt='%Y-%m-%dT%H:%M:%S'
        )
    else:
        # Plain text formatter for development
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
    
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # Set specific log levels
    logging.getLogger("uvicorn").setLevel(logging.WARNING)
    logging.getLogger("motor").setLevel(logging.WARNING)
    
    return logger

def get_logger(name: Optional[str] = None) -> logging.Logger:
    """Get logger instance"""
    if name:
        return logging.getLogger(name)
    return logging.getLogger(__name__)