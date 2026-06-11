#!/usr/bin/env python3
import logging

class LoggerSetup:
    """Class-level configuration for application-wide logging."""

    @classmethod
    def get_logger(cls, name: str) -> logging.Logger:
        """Returns a configured logger with the specified qualified name."""
        logger = logging.getLogger(name)
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                "[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s",
                datefmt="%H:%M:%S",
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            logger.setLevel(logging.INFO)
        return logger
