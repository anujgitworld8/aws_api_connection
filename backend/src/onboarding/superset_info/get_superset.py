import json

from pathlib import Path

from ...common.log_method import application_logger
from ...common.json_responses import debugmessages, infomessages
from ...common.info_log_method import process_logger
from ...common.get_parent_filepath import read_files_from_parent_dir
from ...common.open_json_file import with_open_read_json_file


# Method to fetch report url stored in properties.json file
async def fetch_superset_url():
    archive_viewer_log = application_logger()
    try:
        archive_viewer_log_info = process_logger()
        fileName = read_files_from_parent_dir(3)

        properties = with_open_read_json_file(fileName)

        superSetUrl = properties["superset_url"]
        if superSetUrl == "":
            superset_Url = None
        else:
            superset_Url = superSetUrl

        archive_viewer_log_info.info(infomessages["info_messages"]["5041"])

        return superset_Url

    except Exception as e:
        archive_viewer_log.exception(e, exc_info=True)
        archive_viewer_log.error(debugmessages["debug_messages"]["1976"])
