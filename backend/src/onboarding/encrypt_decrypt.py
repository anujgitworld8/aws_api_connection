import os
import base64

from cryptography.fernet import Fernet

from ..common.run_command import command_run
from ..common.log_method import application_logger
from ..common.json_responses import debugmessages


# Method to generate key for encryption and decryption.
def get_key():
    archive_viewer_log = application_logger()
    try:
        if "nt" in os.name:
            key = command_run("wmic csproduct get uuid")
        else:
            key = command_run("cat /etc/machine-id")

        key = key[:32]
        key = key.encode()
        key = base64.urlsafe_b64encode(key)
        return key
    except Exception as e:
        archive_viewer_log.exception(e, exc_info=True)
        archive_viewer_log.error(debugmessages["debug_messages"]["3003"])


# Method to encrypt data.
def json_encrypt(dbInfo):
    archive_viewer_log = application_logger()
    try:
        key = get_key()
        f = Fernet(key)
        encrypted = f.encrypt(dbInfo.encode("UTF-8"))
        return encrypted
    except Exception as e:
        archive_viewer_log.exception(e, exc_info=True)
        archive_viewer_log.error(debugmessages["debug_messages"]["3004"])


# Method to decrypt data.
def json_decrypt(encrypted):
    archive_viewer_log = application_logger()
    try:
        key = get_key()
        f = Fernet(key)
        decrypted = f.decrypt(encrypted)
        return decrypted.decode("UTF-8")
    except Exception as e:
        archive_viewer_log.exception(e, exc_info=True)
        archive_viewer_log.error(debugmessages["debug_messages"]["3005"])
