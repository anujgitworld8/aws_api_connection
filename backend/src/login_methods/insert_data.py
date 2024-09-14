import base64
from datetime import datetime, timezone, timedelta
from pathlib import Path

from ..common.json_responses import debugmessages
from ..common.log_method import application_logger
from ..common.get_parent_filepath import (
    read_store_data_txt_from_parent_dir,
    read_login_data_txt_from_parent_dir,
)
from .authentication import Auth

auth_handler = Auth()

fileName = read_login_data_txt_from_parent_dir(1)
store_data_filename = read_store_data_txt_from_parent_dir(1)


# Method to insert logged-in user details into login_data.
def insert_data(access_token):
    archive_viewer_log = application_logger()
    try:
        timestamp = datetime.utcnow()

        res1 = auth_handler.decode_token(str(access_token))
        with open(fileName, "r") as f:
            text = f.readlines()
        text

        if len(text) > 0:
            for data in text:
                data1 = data.split(" ")
                if data1[0] == res1:
                    with open(store_data_filename, "a") as file:
                        file.write(f"{data1[1]}" + " " + str(timestamp) + "\n")
                else:
                    with open(fileName, "w") as file1:
                        file1.write(data)

        with open(fileName, "r") as f:
            textdata = f.readlines()
        textdata
        # If user logged-in for more than 30 mins then, user details will be removed from login_data and added to store_data file.
        with open(fileName, "w") as f:
            if len(textdata) > 0:
                for result in textdata:
                    elements = result.split(" ")
                    data1 = elements[2] + elements[3].strip("\n")
                    format_type = "%Y-%m-%d%H:%M:%S.%f"
                    timedata = datetime.strptime(data1, format_type)
                    if timedata >= datetime.utcnow() - timedelta(days=0, minutes=25):
                        f.write(result)

        with open(fileName, "a") as f:
            userid = auth_handler.decode_token(str(access_token))
            bytes_encoded = access_token.encode()
            enc_data = base64.b64encode(bytes_encoded).decode("utf-8")
            f.write(userid + " " + enc_data + " " + str(timestamp) + "\n")
    except Exception as e:
        archive_viewer_log.exception(e, exc_info=True)
        archive_viewer_log.error(debugmessages["debug_messages"]["2058"])
