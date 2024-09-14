import base64

from ..common.get_orm_classes import get_orm_classes
from ..common.json_responses import (
    messages,
    errormessages,
    permissions,
    debugmessages,
    infomessages,
)
from ..common.exceptions import exceptions
from ..common.log_method import application_logger
from ..common.info_log_method import process_logger

from .gen_psswrd import autogen_psswrd


# Method to change the status of specific user.
async def modify_status_new(userinfo, db):
    ormclass_dict = get_orm_classes()
    Rolemaster = ormclass_dict["Rolemaster"]
    Userrole = ormclass_dict["Userrole"]
    Usermaster = ormclass_dict["Usermaster"]

    archive_viewer_log = application_logger()
    archive_viewer_log_info = process_logger()

    user_name = userinfo.username.lower()
    user_status = userinfo.userstatus.lower()

    user_role = (
        db.query(Rolemaster.rolename)
        .join(Userrole, Rolemaster.id == Userrole.rolemasterid)
        .join(Usermaster, Usermaster.id == Userrole.usermasterid)
        .filter(Usermaster.username == user_name)
        .all()
    )

    for role in user_role:
        if role[0] == permissions["roles"]["501"]:
            db.query(Usermaster).filter(Usermaster.username == user_name).update(
                {Usermaster.active: user_status}
            )
            db.commit()
            exceptions(409, "409-A", errormessages["errormessagecode"]["922"])

    user_id = db.query(Usermaster.id).filter(Usermaster.username == user_name).first()

    if user_id is None:
        exceptions(404, None, errormessages["errormessagecode"]["723"])

    rand_psswrd = autogen_psswrd()
    message_bytes = rand_psswrd.encode("ascii")
    base64_bytes = base64.b64encode(message_bytes)
    temp_psswrd = base64_bytes.decode("ascii")

    if user_status == messages["messagecode"]["114"]:
        try:
            db.query(Usermaster).filter(Usermaster.username == user_name).update(
                {
                    Usermaster.psswrd: temp_psswrd,
                    Usermaster.active: messages["messagecode"]["114"],
                    Usermaster.salt: None,
                    Usermaster.wrong_psswrd_cnt: 0,
                }
            )
            db.commit()
            archive_viewer_log_info.info(infomessages["info_messages"]["5026"])
            return messages["returnmessagecode"]["616"]
        except Exception as e:
            archive_viewer_log.exception(e, exc_info=True)
            archive_viewer_log.error(debugmessages["debug_messages"]["3017"])

    elif user_status == messages["messagecode"]["171"]:
        try:
            db.query(Usermaster).filter(Usermaster.username == user_name).update(
                {Usermaster.active: messages["messagecode"]["171"]}
            )
            db.commit()
            archive_viewer_log_info.info(infomessages["info_messages"]["5026"])
            return messages["returnmessagecode"]["616"]
        except Exception as e:
            archive_viewer_log.exception(e, exc_info=True)
            archive_viewer_log.error(debugmessages["debug_messages"]["3017"])

    else:
        exceptions(422, None, errormessages["errormessagecode"]["717"])
