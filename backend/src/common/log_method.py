import logging

from pathlib import Path
from datetime import datetime, timezone

from ..common.json_responses import properties
from ..common.utc import UTCFormatter

formatter = UTCFormatter(
    "%(asctime)s %(levelname)s %(message)s", datefmt="%d/%m/%Y %H:%M:%S"
)


def setup_logger(name, log_file, level):
    if name == "process":
        return application_logger()
    return default_logger(name, log_file, level)


# Method to create log file.
def default_logger(name, log_file, level):
    today = datetime.now()
    dt_string = today.strftime("%d_%m_%Y_%H_%M_%S_%f")
    name = name + dt_string
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger
    else:
        handler = logging.FileHandler(log_file)
        handler.setFormatter(formatter)
        logger.setLevel(level)
        logger.addHandler(handler)
        handler.close()
        return logger


# Method to create error application log file.
def application_logger():
    message_format = UTCFormatter(
        "%(asctime)s %(filename)s -> %(funcName)s() : %(lineno)s %(levelname)s: %(message)s"
    )
    cwd = Path(__file__).parents[4]
    filepath = str(cwd / properties["error_log_path"])

    today = datetime.now()
    dt_string = today.strftime("%d_%b_%Y")
    name = "archiveviewererror_" + dt_string + ".log"

    Path(filepath).mkdir(parents=True, exist_ok=True)
    log_filepath = Path(filepath, name)
    log_fname = str(log_filepath)

    logger = logging.getLogger(log_fname)
    if logger.handlers:
        return logger
    else:
        handler = logging.FileHandler(log_fname)
        handler.setFormatter(message_format)
        logger.setLevel(logging.ERROR)
        logger.addHandler(handler)
        handler.close()
        return logger


archive_viewer_log = application_logger()
