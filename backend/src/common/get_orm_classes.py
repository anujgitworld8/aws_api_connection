from ..common.get_parent_filepath import read_files_from_parent_dir
from ..common.open_json_file import with_open_read_json_file

from .json_responses import messages, errormessages
from .exceptions import exceptions


# Method to get all the ORM classes.
def get_orm_classes():
    file_name = read_files_from_parent_dir(3)
    print("================Config File Name:", file_name) 

    properties = with_open_read_json_file(file_name)
    print("===============Properties:", properties)  # Debugging line

    if (
        properties["metadata_config"]["databaseType"].lower()
        == messages["messagecode"]["187"]
        ):
            from ..orm_classes.get_mysql_orm import get_mysql_orm

            response_dict = get_mysql_orm()
            return response_dict

    else:
        exceptions(404, "404-Y", errormessages["errormessagecode"]["784"])

