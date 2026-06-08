import logging
from pathlib import Path


def setup_logging(log_file: str = "trading_bot.log", level: int = logging.INFO) -> None:
    """Configure app-wide logging.

    Logs both to console and to the given log file.
    """
    log_path = Path(log_file)

    logger = logging.getLogger()
    logger.setLevel(level)

    # Avoid duplicate handlers if setup_logging is called multiple times.
    if logger.handlers:
        return

    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    file_handler = logging.FileHandler(log_path, encoding="utf-8")
    file_handler.setLevel(level)
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

