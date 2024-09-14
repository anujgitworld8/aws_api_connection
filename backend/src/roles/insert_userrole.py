import json

from pathlib import Path
from datetime import datetime, timezone

from ..common.get_orm_classes import get_orm_classes
from ..common.log_method import application_logger
from ..common.json_responses import debugmessages, infomessages, messages
from ..common.info_log_method import process_logger
from ..common.get_parent_filepath import read_files_from_parent_dir
from ..common.open_json_file import with_open_read_json_file


# Method to insert the user roles into userroles table.
async def insert_userroles(usermasterid, roleid, user_id, db):
    archive_viewer_log = application_logger()
    archive_viewer_log_info = process_logger()

    fileName = read_files_from_parent_dir(3)

    properties = with_open_read_json_file(fileName)

    authenticate_type = properties["auth_type"]

    ormclass_dict = get_orm_classes()
    Userrole = ormclass_dict["Userrole"]
    timestamp = datetime.now(timezone.utc)

    # LDAP server.
    if authenticate_type.upper() == messages["messagecode"]["150"]:
        try:
            role_info = Userrole(
                usermasterid=usermasterid,
                rolemasterid=roleid,
                createdate=timestamp,
                created_by=usermasterid,
                last_updated=timestamp,
                last_updated_by=usermasterid,
            )
            db.add(role_info)
            db.commit()
            db.refresh(role_info)

            archive_viewer_log_info.info(infomessages["info_messages"]["5022"])
        except Exception as e:
            archive_viewer_log.exception(e, exc_info=True)
            archive_viewer_log.error(debugmessages["debug_messages"]["2056"])

    # BASIC authentication.
    else:
        try:
            role_info = Userrole(
                usermasterid=usermasterid,
                rolemasterid=roleid,
                createdate=timestamp,
                created_by=user_id,
                last_updated=timestamp,
                last_updated_by=user_id,
            )
            db.add(role_info)
            db.commit()
            db.refresh(role_info)
            archive_viewer_log_info.info(
                infomessages["info_messages"]["5028"], str(roleid)
            )

        except Exception as e:
            archive_viewer_log.exception(e, exc_info=True)
            archive_viewer_log.error(debugmessages["debug_messages"]["1965"])
