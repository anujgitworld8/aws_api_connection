import json
import os

from pathlib import Path
from datetime import datetime, timezone

from ..common.create_jsonfile import (
    # write_ldapconfiguration,
    tables_created_status,
    # update_queryserver_flag,
    metadata_configuration,
    store_skip_superseturl,
)
from ..common.json_responses import messages, errormessages, infomessages
from ..common.exceptions import exceptions
from ..common.info_log_method import process_logger
from ..common.get_parent_filepath import read_files_from_parent_dir
from ..common.open_json_file import with_open_read_json_file


# Method to clear properties.json file and to carete a backup JSON file with previous data.
async def delete_onboard_deatils():
    archive_viewer_log_info = process_logger()
    fileName = read_files_from_parent_dir(3)
    properties = with_open_read_json_file(fileName)

    today = datetime.now()
    dt_string = today.strftime("%d%m%y%H%M%S")

    tempTuple = os.path.splitext(fileName)

    updatedfilename = tempTuple[0] + "_" + dt_string + ".json"
    with open(updatedfilename, "w") as outfile:
        json.dump(properties, outfile, indent=4)

    logintype = properties["auth_type"]

    if len(logintype) == 0:
        logintype = ""

    if logintype.upper() == messages["messagecode"]["151"]:
        metadata_config = {
            "databaseType": "",
            "host": "",
            "port": "",
            "username": "",
            "psswrd": "",
            "databaseName": "",
            "connectionType": "",
            "loginType": "",
        }
        await metadata_configuration(metadata_config)
        await tables_created_status(False)
        # await update_queryserver_flag(False)
        await store_skip_superseturl(False)
        archive_viewer_log_info.info(infomessages["info_messages"]["5003"])
        
        return messages["returnmessagecode"]["639"]

    # elif logintype.upper() == messages["messagecode"]["150"]:
    #     # ldap_configuration = {
    #     #     "dnsIp": "",
    #     #     "port": "",
    #     #     "use_ssl": False,
    #     #     "baseDN": "",
    #     #     "attribute": "",
    #     # }
    #     metadata_config = {
    #         "databaseType": "",
    #         "host": "",
    #         "port": "",
    #         "username": "",
    #         "psswrd": "",
    #         "databaseName": "",
    #         "connectionType": "",
    #         "loginType": "",
    #     }
    #     await metadata_configuration(metadata_config)
    #     # await write_ldapconfiguration(ldap_configuration)
    #     await tables_created_status(False)
    #     # await update_queryserver_flag(False)
    #     await store_skip_superseturl(False)

    #     archive_viewer_log_info.info(infomessages["info_messages"]["5003"])
    #     return messages["returnmessagecode"]["639"]

    # else:
    #     exceptions(404, "404-A", errormessages["errormessagecode"]["869"])
