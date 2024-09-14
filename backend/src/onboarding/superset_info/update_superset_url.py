from ...common.create_jsonfile import store_superseturl
from ...common.json_responses import messages, debugmessages, infomessages
from ...common.info_log_method import process_logger
from ...common.log_method import application_logger


# Method to update report url in properties.json file
async def update_superset_url(item):
    archive_viewer_log = application_logger()
    try:
        archive_viewer_log_info = process_logger()
        await store_superseturl(item.superseturl)

        archive_viewer_log_info.info(infomessages["info_messages"]["5042"])

        return messages["returnmessagecode"]["637"]
    except Exception as e:
        archive_viewer_log.exception(e, exc_info=True)
        archive_viewer_log.error(debugmessages["debug_messages"]["1978"])
