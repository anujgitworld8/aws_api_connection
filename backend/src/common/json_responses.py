import os
import json

from pathlib import Path
from ..common.get_parent_filepath import read_files_from_parent_dir
from ..common.open_json_file import with_open_read_json_file

script_dir = os.path.dirname(__file__)

fileName = read_files_from_parent_dir(3)

properties = with_open_read_json_file(fileName)

# spark_datatypes_file_path = Path(script_dir) / "./spark_datatypes.json"

# spark_types = with_open_read_json_file(spark_datatypes_file_path)


permissions_file_path = Path(script_dir) / "./permissions.json"
permissions = with_open_read_json_file(permissions_file_path)

responses_file_path = Path(script_dir) / "./responses.json"
response = with_open_read_json_file(responses_file_path)


success_file_path = Path(script_dir) / "./success_code.json"

messages = with_open_read_json_file(success_file_path)


error_file_path = Path(script_dir) / "./error_code.json"
errormessages = with_open_read_json_file(error_file_path)


debug_message_file_path = Path(script_dir) / "./log_messages.json"
debugmessages = with_open_read_json_file(debug_message_file_path)


info_messages_file_path = Path(script_dir) / "./info_logmesssages.json"
infomessages = with_open_read_json_file(info_messages_file_path)

log_message_file_path = Path(script_dir) / "./requestlog_messages.json"
logmessages = with_open_read_json_file(log_message_file_path)


# linux_system_libraries_path = Path(script_dir) / "./system_paths.json"
# systempaths = with_open_read_json_file(linux_system_libraries_path)
