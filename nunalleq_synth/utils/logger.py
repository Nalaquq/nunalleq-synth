
# ============================================================================
# nunalleq_synth/utils/logger.py
# ============================================================================
"""Logging utilities for nunalleq-synth."""

import logging
import sys
from pathlib import Path
from typing import Optional


def setup_logger(
    level: int = logging.INFO,
    log_file: Optional[Path] = None,
    format_string: Optional[str] = None,
) -> logging.Logger:
    """Setup application-wide logger.
    
    Args:
        level: Logging level (e.g., logging.INFO, logging.DEBUG).
        log_file: Optional path to log file. If None, logs to console only.
        format_string: Custom format string for log messages.
        
    Returns:
        Configured logger instance.
    """
    if format_string is None:
        format_string = (
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
    
    # Create formatter
    formatter = logging.Formatter(format_string)
    
    # Setup root logger
    root_logger = logging.getLogger("nunalleq_synth")
    root_logger.setLevel(level)
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)
    
    # File handler (optional)
    if log_file:
        log_file.parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)
    
    return root_logger


def get_logger(name: str) -> logging.Logger:
    """Get a logger instance.
    
    Args:
        name: Logger name (typically __name__).
        
    Returns:
        Logger instance.
    """
    return logging.getLogger(f"nunalleq_synth.{name}")

