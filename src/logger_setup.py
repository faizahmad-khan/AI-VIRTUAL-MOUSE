"""
Logging setup for AI Virtual Mouse application.
"""

import logging
import os
from pathlib import Path
from logging.handlers import RotatingFileHandler
from typing import Optional


def setup_logger(
    name: str = "ai_virtual_mouse",
    log_file: Optional[str] = None,
    level: str = "INFO",
    max_bytes: int = 10485760,  # 10MB
    backup_count: int = 3,
    console: bool = True
) -> logging.Logger:
    """
    Setup logger with file and console handlers.
    
    Args:
        name: Logger name
        log_file: Path to log file (None for default)
        level: Logging level (DEBUG, INFO, WARNING, ERROR)
        max_bytes: Maximum log file size before rotation
        backup_count: Number of backup files to keep
        console: Whether to also log to console
    
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    
    # Clear existing handlers to avoid duplicates
    logger.handlers.clear()
    
    # Set logging level
    log_level = getattr(logging, level.upper(), logging.INFO)
    logger.setLevel(log_level)
    
    # Create formatters
    detailed_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    simple_formatter = logging.Formatter(
        '%(levelname)s - %(message)s'
    )
    
    # File handler with rotation
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=max_bytes,
            backupCount=backup_count
        )
        file_handler.setLevel(log_level)
        file_handler.setFormatter(detailed_formatter)
        logger.addHandler(file_handler)
    
    # Console handler
    if console:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(log_level)
        console_handler.setFormatter(simple_formatter)
        logger.addHandler(console_handler)
    
    return logger


class PerformanceLogger:
    """Logger for tracking performance metrics."""
    
    def __init__(self, logger: logging.Logger):
        self.logger = logger
        self.frame_count = 0
        self.total_processing_time = 0.0
    
    def log_frame(self, processing_time: float):
        """Log frame processing time."""
        self.frame_count += 1
        self.total_processing_time += processing_time
        
        if self.frame_count % 100 == 0:
            avg_time = self.total_processing_time / self.frame_count
            fps = 1.0 / avg_time if avg_time > 0 else 0
            self.logger.debug(
                f"Performance: {self.frame_count} frames, "
                f"Avg time: {avg_time*1000:.2f}ms, FPS: {fps:.2f}"
            )
    
    def reset(self):
        """Reset performance counters."""
        self.frame_count = 0
        self.total_processing_time = 0.0


if __name__ == "__main__":
    # Test the logger
    logger = setup_logger(
        log_file="logs/test.log",
        level="DEBUG"
    )
    
    logger.debug("This is a debug message")
    logger.info("This is an info message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")
