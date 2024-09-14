import base64

from sqlalchemy import func
from datetime import datetime, timezone

from ..common.get_orm_classes import get_orm_classes
from ..common.exceptions import exceptions
from ..users.gen_psswrd import autogen_psswrd
from ..common.json_responses import (
    errormessages,
    messages,
    debugmessages,
    infomessages,
)
from ..common.log_method import application_logger
from ..common.info_log_method import process_logger
from ..common.get_parent_filepath import read_files_from_parent_dir
from ..common.open_json_file import with_open_read_json_file

# Method to insert the user data into usermaster table.
async def insert_userdetails(item, user_id, db):
    ormclass_dict = get_orm_classes()
    Usermaster = ormclass_dict["Usermaster"]

    archive_viewer_log = application_logger()
    archive_viewer_log_info = process_logger()

    fileName = read_files_from_parent_dir(3)

    properties = with_open_read_json_file(fileName)

    authenticate_type = properties["auth_type"]
    timestamp = datetime.now(timezone.utc)

    # LDAP server.
    if authenticate_type.upper() == messages["messagecode"]["150"]:
        try:
            user_details = Usermaster(
                fullname=item.fullname,
                username=item.userName,
                useremail=item.mail,
                active=messages["messagecode"]["114"],
                created_by=user_id,
                last_updated=timestamp,
                last_updated_by=user_id,
                last_login=None,
            )
            db.add(user_details)
            db.commit()
            db.refresh(user_details)

            userid = db.query(func.max(Usermaster.id)).scalar()
            if userid is not None:
                usermasterid = userid
                return usermasterid
            else:
                exceptions(404, "404-E", errormessages["errormessagecode"]["746"])

        except Exception as e:
            archive_viewer_log.exception(e, exc_info=True)
            archive_viewer_log.error(debugmessages["debug_messages"]["2056"])

    # BASIC authentication.
    else:
        rand_psswrd = autogen_psswrd()
        message_bytes = rand_psswrd.encode("ascii")
        base64_bytes = base64.b64encode(message_bytes)
        temp_psswrd = base64_bytes.decode("ascii")
        try:
            user_details = Usermaster(
                fullname=item.name,
                username=item.username.lower(),
                psswrd=temp_psswrd,
                useremail=item.email,
                active=messages["messagecode"]["114"],
                created_date=timestamp,
                created_by=user_id,
                last_updated=timestamp,
                last_updated_by=user_id,
                wrong_psswrd_cnt=0,
            )
            db.add(user_details)
            db.commit()
            db.refresh(user_details)
            userid = (
                db.query(Usermaster.id)
                .filter(Usermaster.username == item.username.lower())
                .first()
            )

            if userid is not None:
                usermasterid = userid[0]
                return usermasterid
            else:
                exceptions(404, "404-E", errormessages["errormessagecode"]["746"])
            archive_viewer_log_info.info(
                infomessages["info_messages"]["5027"], item.username
            )

        except Exception as e:
            archive_viewer_log.exception(e, exc_info=True)
            archive_viewer_log.error(debugmessages["debug_messages"]["3009"])
