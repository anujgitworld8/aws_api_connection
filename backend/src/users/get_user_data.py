import base64
import json

from pathlib import Path

from ..common.json_responses import debugmessages, messages
from ..common.log_method import application_logger
from ..common.get_parent_filepath import read_files_from_parent_dir
from ..common.open_json_file import with_open_read_json_file


# Method to get all user details from usermaster table according to user role.
async def get_userdata(userdetails, userroles):
    archive_viewer_log = application_logger()
    try:
        if userdetails is not None or userroles != []:
            user_role = userroles[0][0]

            fileName = read_files_from_parent_dir(3)
            properties = with_open_read_json_file(fileName)

            authType = properties["auth_type"]
            if authType == messages["messagecode"]["151"]:
                if userdetails[3] == messages["messagecode"]["114"]:
                    base64_message = userdetails[2]
                    base64_bytes = base64_message.encode("ascii")
                    message_bytes = base64.b64decode(base64_bytes)
                    temp_psswrd = message_bytes.decode("ascii")
                    result = {
                        "id": userdetails[0],
                        "name": userdetails[9],
                        "username": userdetails[1].lower(),
                        "psswrd": temp_psswrd,
                        "isActive": userdetails[3],
                        "createdDate": userdetails[4],
                        "createdBy": userdetails[5],
                        "updatedDate": userdetails[6],
                        "updatedBy": userdetails[7],
                        "email": userdetails[8],
                        "role": user_role,
                    }
                else:
                    result = {
                        "id": userdetails[0],
                        "name": userdetails[9],
                        "username": userdetails[1].lower(),
                        "isActive": userdetails[3],
                        "createdDate": userdetails[4],
                        "createdBy": userdetails[5],
                        "updatedDate": userdetails[6],
                        "updatedBy": userdetails[7],
                        "email": userdetails[8],
                        "role": user_role,
                    }

                return result
            elif authType == messages["messagecode"]["150"]:
                result = {
                    "id": userdetails[0],
                    "name": userdetails[9],
                    "username": userdetails[1],
                    "isActive": userdetails[3],
                    "createdDate": userdetails[4],
                    "createdBy": userdetails[5],
                    "updatedDate": userdetails[6],
                    "updatedBy": userdetails[7],
                    "email": userdetails[8],
                    "role": user_role,
                }
                return result
            else:
                archive_viewer_log.error(debugmessages["debug_messages"]["3236"])

        else:
            return None
    except Exception as e:
        archive_viewer_log.exception(e, exc_info=True)
        archive_viewer_log.error(debugmessages["debug_messages"]["1967"])
