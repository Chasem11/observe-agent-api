"""
Logging configuration for the application
"""
import logging
import sys


# Configure root logger once
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s [%(name)s] %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)


def get_logger(name: str) -> logging.Logger:
    """Get a logger instance for a module"""
    return logging.getLogger(name)
