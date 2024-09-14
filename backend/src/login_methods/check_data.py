import base64

from datetime import datetime, timezone, timedelta

from ..common.exceptions import exceptions
from ..common.json_responses import errormessages, debugmessages
from ..common.log_method import application_logger
from ..common.get_parent_filepath import read_store_data_txt_from_parent_dir


# Method to check if the user previously logged-in or not.
def data_status(token):
    bytes_encoded = token.encode()
    enc_data = base64.b64encode(bytes_encoded).decode("utf-8")

    fileName = read_store_data_txt_from_parent_dir(1)

    archive_viewer_log = application_logger()
    textdata = None
    text = None
    try:
        with open(fileName, "r") as f:
            text = f.readlines()

        with open(fileName, "r") as f:
            textdata = f.read()

        with open(fileName, "w") as f:
            if len(text) > 0:
                for result in text:
                    elements = result.split(" ")
                    data = elements[1] + " " + elements[2].strip("\n")
                    format_type = "%Y-%m-%d %H:%M:%S.%f"
                    timedata = datetime.strptime(data, format_type)
                    if timedata >= datetime.utcnow() - timedelta(days=0, minutes=25):
                        f.write(result)

    except Exception as e:
        archive_viewer_log.exception(e, exc_info=True)
        archive_viewer_log.error(debugmessages["debug_messages"]["2057"])

    if enc_data in textdata:
        exceptions(440, None, errormessages["errormessagecode"]["821"])
