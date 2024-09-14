from ..common.json_responses import debugmessages
from .log_method import application_logger


# Method to validate if metadata database parameters doesn't have empty values
def is_empty_value(host, port, username, psswrd, dbname):
    archive_viewer_log = application_logger()
    try:
        if (
            len(host)
            and len(str(port))
            and len(username)
            and len(psswrd)
            and len(dbname)
        ) == 0:
            return False
        else:
            return True
    except Exception as e:
        archive_viewer_log.exception(e, exc_info=True)
        archive_viewer_log.error(debugmessages["debug_messages"]["3250"])


# Method to validate if sqlite database parameters doesn't have empty values
def sqlite_is_empty_value(dbname):
    archive_viewer_log = application_logger()
    try:
        if len(dbname) == 0:
            return False
        else:
            return True
    except Exception as e:
        archive_viewer_log.exception(e, exc_info=True)
        archive_viewer_log.error(debugmessages["debug_messages"]["3250"])
