import logging
from logging.handlers import TimedRotatingFileHandler
import os
from pathlib import Path


def setup():
    """Set up logging"""
    log_file = Path(os.getenv("LOCALAPPDATA")) / "utf8csv.log"
    handler = TimedRotatingFileHandler(filename=log_file, when="w6", backupCount=4, delay=True)
    log_format = "[%(asctime)s] [%(name)s.pid%(process)d] %(levelname)s: %(message)s"
    logging.basicConfig(handlers=[handler], format=log_format, level=logging.INFO)


def read_logs() -> tuple[list[Path], str]:
    """Return a list of old log files and the latest log file's full text"""
    log_files = sorted(Path(os.getenv("LOCALAPPDATA")).glob("utf8csv*.log"), key=lambda f: f.stat().st_mtime)
    return log_files[:-1], log_files[-1].read_text(errors="backslashreplace")
