from ..common.exceptions import exceptions
from ..common.json_responses import (
    errormessages,
    messages,
    debugmessages,
    errormessages,
    infomessages,
)
from ..common.get_orm_classes import get_orm_classes
from ..common.log_method import application_logger
from ..common.info_log_method import process_logger


# Method to update the wrong psswrd count in Usermaster table.
def update_count(username, rolename, db):
    archive_viewer_log_info = process_logger()
    ormclass_dict = get_orm_classes()
    Usermaster = ormclass_dict["Usermaster"]

    count_val = 0

    count_val = (
        db.query(Usermaster.wrong_psswrd_cnt)
        .filter(Usermaster.username == username)
        .first()
    )
    archive_viewer_log = application_logger()
    if count_val is None:
        archive_viewer_log_info.info(infomessages["info_messages"]["5109"])
    elif count_val[0] < 3:
        try:
            db.query(Usermaster).filter(Usermaster.username == username).update(
                {Usermaster.wrong_psswrd_cnt: count_val[0] + 1}
            )
            db.commit()
        except Exception as e:
            archive_viewer_log.exception(e, exc_info=True)
            archive_viewer_log.error(debugmessages["debug_messages"]["2060"])
    else:
        try:
            db.query(Usermaster).filter(Usermaster.username == username).update(
                {
                    Usermaster.psswrd: None,
                    Usermaster.active: messages["messagecode"]["172"],
                }
            )
            db.commit()
        except Exception as e:
            archive_viewer_log.exception(e, exc_info=True)
            archive_viewer_log.error(debugmessages["debug_messages"]["2060"])
        if rolename != messages["messagecode"]["152"]:
            exceptions(419, "419-B", errormessages["errormessagecode"]["811"])
        else:
            exceptions(404, "404-D", errormessages["errormessagecode"]["925"])
