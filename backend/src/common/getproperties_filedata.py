import json
from pathlib import Path

from ..common.exceptions import exceptions
from ..common.json_responses import messages, errormessages

from .validate_db_parameters import is_empty_value, sqlite_is_empty_value
from ..common.open_json_file import with_open_read_json_file
from ..common.get_parent_filepath import read_files_from_parent_dir


# Method to check all the metadata information is present or not.
async def properties_file_details():
    fileName = read_files_from_parent_dir(3)
    properties = with_open_read_json_file(fileName)

    databaseType = properties["metadata_config"]["databaseType"].lower()
    host = properties["metadata_config"]["host"]
    port = properties["metadata_config"]["port"]
    username = properties["metadata_config"]["username"]
    psswrd = properties["metadata_config"]["psswrd"]
    databaseName = properties["metadata_config"]["databaseName"]
    createTableStatus = properties["tables_created"]

    if len(databaseType) != 0 and createTableStatus == True:
        if (
            databaseType == messages["messagecode"]["184"]
            or databaseType == messages["messagecode"]["185"]
            or databaseType == messages["messagecode"]["186"]
            or databaseType == messages["messagecode"]["187"]
            or databaseType == messages["messagecode"]["214"]
        ):
            check = is_empty_value(host, port, username, psswrd, databaseName)
            return check

        elif databaseType == messages["messagecode"]["188"]:
            check = sqlite_is_empty_value(databaseName)
            return check

        else:
            exceptions(404, "404-Y", errormessages["errormessagecode"]["784"])
    else:
        return False
