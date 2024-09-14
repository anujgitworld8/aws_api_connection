import logging

from pathlib import Path
from datetime import datetime, timezone
from ..common.utc import UTCFormatter

from ..common.json_responses import properties


def process_logger():

    message_format = UTCFormatter(
        "%(asctime)s %(filename)s -> %(funcName)s() : %(lineno)s %(levelname)s: %(message)s"
    )
    cwd = Path(__file__).parents[4]
    filepath = str(cwd / properties["error_log_path"])
    today = datetime.now()
    dt_string = today.strftime("%d_%b_%Y")
    name = "archiveviewerinfo_" + dt_string + ".log"

    Path(filepath).mkdir(parents=True, exist_ok=True)
    log_filepath = Path(filepath, name)
    log_fname = str(log_filepath)

    logger = logging.getLogger(log_fname)
    if logger.handlers:
        return logger
    else:
        handler = logging.FileHandler(log_fname)
        handler.setFormatter(message_format)
        logger.setLevel(logging.INFO)
        logger.addHandler(handler)
        handler.close()
        return logger


archive_viewer_log_info = process_logger()
