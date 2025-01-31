import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

LOG_FORMAT = "%(asctime)s | %(name)-12s | %(levelname)-8s | %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def setup_logger(
    name: str,
    log_dir: Path,
    log_level: int = logging.INFO,
    file_size: int = 10 * 1024 * 1024,
    backup_count: int = 5,
):
    logger = logging.getLogger(name)
    logger.setLevel(log_level)

    if not logger.handlers:
        # console logger
        console_logger = logging.StreamHandler()
        console_logger.setFormatter(logging.Formatter(LOG_FORMAT, datefmt=DATE_FORMAT))
        logger.addHandler(console_logger)

        # file handler
        log_dir.mkdir(parents=True, exist_ok=True)
        file_handler = RotatingFileHandler(
            log_dir / f"{name}.log",
            maxBytes=file_size,
            backupCount=backup_count,
            encoding="utf-8",
        )
        file_handler.setFormatter(logging.Formatter(LOG_FORMAT, datefmt=DATE_FORMAT))
        logger.addHandler(file_handler)

    return logger
