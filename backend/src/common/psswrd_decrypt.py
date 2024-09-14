import base64

from ..common.log_method import application_logger
from ..common.json_responses import errormessages
from ..onboarding.encrypt_decrypt import json_decrypt


# Method to decrypt the encrypted database psswrd
def psswrd_decrypt(psswd):
    archive_viewer_log = application_logger()
    if len(psswd) == 0:
        archive_viewer_log.error(errormessages["errormessagecode"]["905"])
        return None
    else:
        back_to_bytes = base64.b64decode(psswd)
        decrypted_psswrd = json_decrypt(back_to_bytes)
        return decrypted_psswrd
