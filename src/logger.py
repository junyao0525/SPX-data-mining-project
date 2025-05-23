# loggers.py
import logging
import os
from pathlib import Path

def setup_logger(
    log_name : str,
    log_level: str = "INFO",
    log_dir  : str = "logs"
):
  
    Path(log_dir).mkdir(parents=True, exist_ok=True)
    logger = logging.getLogger(log_name)
    if not logger.hasHandlers():
        logger.setLevel(log_level)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler = logging.FileHandler(os.path.join(log_dir, f"{log_name}.log"))
        file_handler.setFormatter(formatter)
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        logger.addHandler(stream_handler)
    return logger

def info_logger():
    return setup_logger("info", log_level="INFO")

def error_logger():
    return setup_logger("error", log_level="ERROR")


def download_logger():
    return setup_logger("download", log_level="INFO")

infoLog = info_logger()
errorLog = error_logger()
downloadLog = download_logger()

