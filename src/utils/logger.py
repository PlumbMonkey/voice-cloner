"""
Logging utility for Voice Cloner
"""
import logging
from pathlib import Path
from typing import Optional
import sys
import io

# Force UTF-8 encoding early
if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except:
        pass


class Logger:
    """Unified logging system using Rich for pretty output"""

    def __init__(
        self, name: str = "VoiceCloner", log_file: Optional[str] = None
    ):
        try:
            from rich.logging import RichHandler
            from rich.console import Console
            
            self.logger = logging.getLogger(name)
            self.logger.setLevel(logging.DEBUG)

            # Remove existing handlers
            self.logger.handlers.clear()

            # Console handler with Rich formatting
            try:
                console_handler = RichHandler(
                    console=Console(force_terminal=True, force_unicode=True, legacy_windows=False),
                    show_time=True,
                    show_level=True,
                    show_path=True,
                )
            except:
                # Fallback if Rich fails
                console_handler = logging.StreamHandler(sys.stdout)
                
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
                try:
                    file_handler = logging.FileHandler(log_file, encoding='utf-8')
                except:
                    file_handler = logging.FileHandler(log_file)
                file_handler.setLevel(logging.DEBUG)
                file_handler.setFormatter(formatter)
                self.logger.addHandler(file_handler)
        except Exception as e:
            # Ultimate fallback - basic logging
            self.logger = logging.getLogger(name)
            self.logger.setLevel(logging.DEBUG)
            self.logger.handlers.clear()
            handler = logging.StreamHandler(sys.stdout)
            handler.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
            self.logger.addHandler(handler)

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
