import os
import hashlib

from ..common.json_responses import debugmessages
from ..common.log_method import application_logger


# Method to generate hashed psswrd and salt.
def hashpsswrd(psswrd):
    archive_viewer_log = application_logger()
    try:
        salt = os.urandom(32)
        encoded_psswrd = psswrd.encode()
        digest = hashlib.pbkdf2_hmac("sha512", encoded_psswrd, salt, 10000)
        hex_hash = digest.hex()
        hashedpsswrd = hex_hash
        return hashedpsswrd, salt
    except Exception as e:
        archive_viewer_log.exception(e, exc_info=True)
        archive_viewer_log.error(debugmessages["debug_messages"]["1968"])
