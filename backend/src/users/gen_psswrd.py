import secrets
import string

from ..common.log_method import application_logger
from ..common.json_responses import debugmessages, infomessages
from ..common.info_log_method import process_logger


# Method to generate temp psswrd.
def autogen_psswrd():
    archive_viewer_log = application_logger()
    try:
        archive_viewer_log_info = process_logger()
        stringSource = string.ascii_letters + string.digits + string.punctuation

        psswrd = secrets.choice(string.ascii_lowercase)
        psswrd += secrets.choice(string.ascii_uppercase)
        psswrd += secrets.choice(string.digits)
        psswrd += secrets.choice(string.punctuation)

        for _ in range(10):
            psswrd += secrets.choice(stringSource)

        char_list = list(psswrd)
        secrets.SystemRandom().shuffle(char_list)
        psswrd = "".join(char_list)

        archive_viewer_log_info.info(infomessages["info_messages"]["5033"])
        return psswrd
    except Exception as e:
        archive_viewer_log.exception(e, exc_info=True)
        archive_viewer_log.error(debugmessages["debug_messages"]["3021"])
