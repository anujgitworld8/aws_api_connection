from ...common.create_jsonfile import store_skip_superseturl, store_superseturl
from ...common.json_responses import messages, debugmessages, infomessages, errormessages
from ...common.log_method import application_logger
from ...common.info_log_method import process_logger
from ...common.exceptions import exceptions
from pydantic import AnyUrl, ValidationError

# Method to add report url
async def store_url(item, skip):
    archive_viewer_log = application_logger()
    try:
        archive_viewer_log_info = process_logger()
        if skip == True:
            await store_skip_superseturl(skip)
            await store_superseturl("")
            return messages["returnmessagecode"]["647"]
        else:
            if AnyUrl(item.superseturl):
                await store_skip_superseturl(skip)
                await store_superseturl(item.superseturl)

                archive_viewer_log_info.info(infomessages["info_messages"]["5042"])
                return messages["returnmessagecode"]["635"]
    except ValidationError as ve:
        exceptions(400, "400-A", errormessages["errormessagecode"]["1031"])
        archive_viewer_log.exception(ve, exc_info=True)
        archive_viewer_log.error(debugmessages["debug_messages"]["1977"])
    except Exception as e:
        archive_viewer_log.exception(e, exc_info=True)
        archive_viewer_log.error(debugmessages["debug_messages"]["1977"])
