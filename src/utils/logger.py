"""
Logging utility for Voice Cloner
"""
import logging
from pathlib import Path
from typing import Optional
from rich.logging import RichHandler
from rich.console import Console
import sys
import io


class Logger:
    """Unified logging system using Rich for pretty output"""

    def __init__(
        self, name: str = "VoiceCloner", log_file: Optional[str] = None
    ):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)

        # Remove existing handlers
        self.logger.handlers.clear()

        # Force UTF-8 encoding for console output on Windows
        if sys.stdout.encoding and 'utf' not in sys.stdout.encoding.lower():
            sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
        if sys.stderr.encoding and 'utf' not in sys.stderr.encoding.lower():
            sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

        # Console handler with Rich formatting
        console_handler = RichHandler(
            console=Console(force_terminal=True, force_unicode=True),
            show_time=True,
            show_level=True,
            show_path=True,
        )
        console_handler.setLevel(logging.DEBUG)

        # Formatter
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        console_handler.setFormatter(formatter)

        self.logger.addHandler(console_handler)

        # File handler if specified
        if log_file:
            log_path = Path(log_file)
            log_path.parent.mkdir(parents=True, exist_ok=True)
            file_handler = logging.FileHandler(log_file, encoding='utf-8')
            file_handler.setLevel(logging.DEBUG)
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)

    def debug(self, msg: str, *args, **kwargs):
        self.logger.debug(msg, *args, **kwargs)

    def info(self, msg: str, *args, **kwargs):
        self.logger.info(msg, *args, **kwargs)

    def warning(self, msg: str, *args, **kwargs):
        self.logger.warning(msg, *args, **kwargs)

    def error(self, msg: str, *args, **kwargs):
        self.logger.error(msg, *args, **kwargs)

    def critical(self, msg: str, *args, **kwargs):
        self.logger.critical(msg, *args, **kwargs)


# Create default logger instance
logger = Logger("VoiceCloner", log_file="./logs/voice_cloner.log")
