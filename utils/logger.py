"""
Logging module for the OCR tool.

This module provides logging functionality for the OCR tool,
including configurable console and file logging.
"""
import logging
import sys
from pathlib import Path
from typing import Optional, Dict


class LoggerConfig:
    """
    Configuration constants for logging.
    
    This class provides default values and constants for
    configuring loggers throughout the application.
    """
    
    DEFAULT_NAME: str = "ocr_tool"
    DEFAULT_LEVEL: int = logging.INFO
    DEFAULT_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # Log levels mapping for easier configuration
    LOG_LEVELS: Dict[str, int] = {
        "debug": logging.DEBUG,
        "info": logging.INFO,
        "warning": logging.WARNING,
        "error": logging.ERROR,
        "critical": logging.CRITICAL
    }


def setup_logger(
    name: str = LoggerConfig.DEFAULT_NAME,
    log_file: Optional[Path] = None,
    level: int = LoggerConfig.DEFAULT_LEVEL,
    log_format: Optional[str] = None,
    propagate: bool = False
) -> logging.Logger:
    """
    Set up and configure a logger with console and optional file output.
    
    This function creates a logger with the specified name and configures
    it with handlers for console output and optionally file output.
    
    Args:
        name: The name of the logger.
        log_file: The path to the log file. If None, logs will only be sent to stdout.
        level: The logging level (e.g., logging.INFO, logging.DEBUG).
        log_format: The log format string. If None, a default format will be used.
        propagate: Whether the logger should propagate messages to parent loggers.
        
    Returns:
        A configured logger instance.
    """
    # Use default format if none provided
    if log_format is None:
        log_format = LoggerConfig.DEFAULT_FORMAT
    
    formatter = logging.Formatter(log_format)
    
    # Get or create logger
    logger = logging.getLogger(name)
    
    # Clear any existing handlers to avoid duplicates
    if logger.handlers:
        logger.handlers.clear()
    
    # Set level and propagation
    logger.setLevel(level)
    logger.propagate = propagate
    
    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # Create file handler if log_file is provided
    if log_file:
        try:
            # Ensure the directory exists
            log_file.parent.mkdir(parents=True, exist_ok=True)
            
            file_handler = logging.FileHandler(log_file)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
        except Exception as e:
            # Log to console if file handler creation fails
            logger.warning(f"Failed to create log file at {log_file}: {str(e)}")
            logger.warning("Continuing with console logging only")
    
    return logger


# Create a default logger for module-level logging
logger = setup_logger()


def get_logger(
    name: str, 
    level: Optional[int] = None,
    log_file: Optional[Path] = None
) -> logging.Logger:
    """
    Get a configured logger with the specified name.
    
    This is a convenience function for getting a logger with a specific
    name while inheriting the default configuration.
    
    Args:
        name: The name of the logger.
        level: Optional logging level. If None, uses the default level.
        log_file: Optional path to a log file.
        
    Returns:
        A configured logger instance.
    """
    return setup_logger(
        name=name,
        level=level or LoggerConfig.DEFAULT_LEVEL,
        log_file=log_file
    )
