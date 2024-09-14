from datetime import datetime, timezone

from ..common.get_orm_classes import get_orm_classes
from ..common.json_responses import messages, debugmessages, infomessages
from ..common.log_method import application_logger
from ..common.info_log_method import process_logger


# Method to update the specific user details with userId.
async def delete_specificuser(usermail, username, delete_user_id, userid, db):
    archive_viewer_log = application_logger()
    try:
        archive_viewer_log_info = process_logger()
        ormclass_dict = get_orm_classes()
        Usermaster = ormclass_dict["Usermaster"]
        Userrole = ormclass_dict["Userrole"]

        timestamp = datetime.now(timezone.utc)

        if usermail is not None:
            updated_username = username + "_" + str(userid)
            updated_email = usermail + "_" + str(userid)
            try:
                db.query(Usermaster).filter(Usermaster.id == userid).update(
                    {
                        Usermaster.username: updated_username,
                        Usermaster.useremail: updated_email,
                        Usermaster.active: messages["messagecode"]["113"],
                        Usermaster.last_updated: timestamp,
                        Usermaster.last_updated_by: delete_user_id,
                    }
                )
                db.commit()

                archive_viewer_log_info.info(
                    infomessages["info_messages"]["5030"], username
                )
            except Exception as e:
                archive_viewer_log.exception(e, exc_info=True)
                archive_viewer_log.error(debugmessages["debug_messages"]["3231"])

            delete_role = (
                db.query(Userrole).filter(Userrole.usermasterid == userid).first()
            )
            if delete_role is not None:
                try:
                    db.delete(delete_role)
                    db.commit()

                    archive_viewer_log_info.info(infomessages["info_messages"]["5031"])
                except Exception as e:
                    archive_viewer_log.exception(e, exc_info=True)
                    archive_viewer_log.error(debugmessages["debug_messages"]["1963"])
            else:
                archive_viewer_log.error(
                    debugmessages["debug_messages"]["3229"], str(userid)
                )
        else:
            updated_username = username + "_" + str(userid)

            try:
                db.query(Usermaster).filter(Usermaster.id == userid).update(
                    {
                        Usermaster.username: updated_username,
                        Usermaster.active: messages["messagecode"]["113"],
                        Usermaster.last_updated: timestamp,
                        Usermaster.last_updated_by: delete_user_id,
                    }
                )
                db.commit()

                archive_viewer_log_info.info(
                    infomessages["info_messages"]["5077"], username
                )
            except Exception as e:
                archive_viewer_log.exception(e, exc_info=True)
                archive_viewer_log.error(debugmessages["debug_messages"]["3231"])

            delete_role = (
                db.query(Userrole).filter(Userrole.usermasterid == userid).first()
            )

            if delete_role is not None:
                try:
                    db.delete(delete_role)
                    db.commit()

                    archive_viewer_log_info.info(infomessages["info_messages"]["5031"])
                except Exception as e:
                    archive_viewer_log.exception(e, exc_info=True)
                    archive_viewer_log.error(debugmessages["debug_messages"]["1963"])
            else:
                archive_viewer_log.error(
                    debugmessages["debug_messages"]["3229"], str(userid)
                )

    except Exception as e:
        archive_viewer_log.exception(e, exc_info=True)
        archive_viewer_log.error(debugmessages["debug_messages"]["1969"])
