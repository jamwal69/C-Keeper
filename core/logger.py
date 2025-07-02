"""
Logging configuration for C-Keeper
"""

import logging
import os
from datetime import datetime
from pathlib import Path

def setup_logging(log_level: str = 'INFO', log_file: str = None):
    """
    Setup logging configuration
    
    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR)
        log_file: Log file path
    """
    # Create logs directory if it doesn't exist
    if log_file:
        log_dir = os.path.dirname(log_file)
        os.makedirs(log_dir, exist_ok=True)
    else:
        os.makedirs('logs', exist_ok=True)
        log_file = f'logs/ckeeper_{datetime.now().strftime("%Y%m%d")}.log'
    
    # Configure logging format
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    date_format = '%Y-%m-%d %H:%M:%S'
    
    # Create formatter
    formatter = logging.Formatter(log_format, date_format)
    
    # Setup file handler
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(formatter)
    
    # Setup console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    
    # Configure root logger
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        handlers=[file_handler, console_handler],
        format=log_format,
        datefmt=date_format
    )
    
    # Set specific loggers
    logging.getLogger('requests').setLevel(logging.WARNING)
    logging.getLogger('urllib3').setLevel(logging.WARNING)
    
    logging.info(f"Logging initialized - Level: {log_level}, File: {log_file}")

class CKeeperLogger:
    """Custom logger for C-Keeper operations"""
    
    def __init__(self, name: str):
        self.logger = logging.getLogger(name)
    
    def debug(self, message: str):
        """Log debug message"""
        self.logger.debug(message)
    
    def info(self, message: str):
        """Log info message"""
        self.logger.info(message)
    
    def warning(self, message: str):
        """Log warning message"""
        self.logger.warning(message)
    
    def error(self, message: str):
        """Log error message"""
        self.logger.error(message)
    
    def critical(self, message: str):
        """Log critical message"""
        self.logger.critical(message)
    
    def log_operation(self, operation: str, target: str, result: str, 
                     level: str = 'INFO', **kwargs):
        """
        Log an operation with structured data
        
        Args:
            operation: Type of operation
            target: Target of operation
            result: Result of operation
            level: Log level
            **kwargs: Additional data to log
        """
        extra_data = ' '.join([f"{k}={v}" for k, v in kwargs.items()])
        message = f"[{operation}] Target: {target} | Result: {result}"
        if extra_data:
            message += f" | {extra_data}"
        
        log_method = getattr(self.logger, level.lower())
        log_method(message)
    
    def log_security_event(self, event_type: str, description: str, 
                          severity: str = 'INFO', **kwargs):
        """
        Log a security event
        
        Args:
            event_type: Type of security event
            description: Description of event
            severity: Severity level
            **kwargs: Additional event data
        """
        extra_data = ' '.join([f"{k}={v}" for k, v in kwargs.items()])
        message = f"[SECURITY][{event_type}] {description}"
        if extra_data:
            message += f" | {extra_data}"
        
        log_method = getattr(self.logger, severity.lower())
        log_method(message)
