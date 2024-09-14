from datetime import datetime, timezone

from ..common.get_orm_classes import get_orm_classes
from ..common.exceptions import exceptions
from ..common.json_responses import (
    errormessages,
    permissions,
    debugmessages,
    infomessages,
)
from ..common.log_method import application_logger
from ..common.info_log_method import process_logger

from .check_role import check_role


# Method to update specific user using "Super User" role.
async def updatewith_superrole(user_id, info, usermasterid, db):
    ormclass_dict = get_orm_classes()
    Rolemaster = ormclass_dict["Rolemaster"]
    Userrole = ormclass_dict["Userrole"]
    Usermaster = ormclass_dict["Usermaster"]

    archive_viewer_log = application_logger()
    archive_viewer_log_info = process_logger()

    timestamp = datetime.now(timezone.utc)
    role_id = info.roleId

    to_be_updated_userrole = await check_role(usermasterid, db)
    if to_be_updated_userrole == permissions["roles"]["502"]:
        role_name = (
            db.query(Rolemaster.rolename).filter(Rolemaster.id == role_id).first()
        )

        if role_name is None:
            exceptions(404, "404-C", errormessages["errormessagecode"]["749"])
        else:
            if role_name.rolename == permissions["roles"]["502"]:
                try:
                    db.query(Usermaster).filter(Usermaster.id == usermasterid).update(
                        {
                            Usermaster.fullname: info.name,
                            Usermaster.useremail: info.email,
                            Usermaster.last_updated: timestamp,
                            Usermaster.last_updated_by: user_id,
                        }
                    )
                    db.commit()

                    db.query(Userrole).filter(
                        Userrole.usermasterid == usermasterid
                    ).update(
                        {
                            Userrole.rolemasterid: role_id,
                            Userrole.last_updated: timestamp,
                            Userrole.last_updated_by: user_id,
                        }
                    )
                    db.commit()

                    archive_viewer_log_info.info(
                        infomessages["info_messages"]["5029"], str(usermasterid)
                    )

                except Exception as e:
                    archive_viewer_log.exception(e, exc_info=True)
                    archive_viewer_log.error(debugmessages["debug_messages"]["3014"])
            else:
                exceptions(404, "404-H", errormessages["errormessagecode"]["748"])

    elif to_be_updated_userrole == permissions["roles"]["501"]:
        if int(usermasterid) == int(user_id):
            role_name = (
                db.query(Rolemaster.rolename).filter(Rolemaster.id == role_id).first()
            )

            if role_name is None:
                exceptions(404, "404-C", errormessages["errormessagecode"]["749"])
            else:
                if role_name.rolename == permissions["roles"]["501"]:
                    try:
                        db.query(Usermaster).filter(
                            Usermaster.id == usermasterid
                        ).update(
                            {
                                Usermaster.fullname: info.name,
                                Usermaster.useremail: info.email,
                                Usermaster.last_updated: timestamp,
                                Usermaster.last_updated_by: user_id,
                            }
                        )
                        db.commit()

                        archive_viewer_log_info.info(
                            infomessages["info_messages"]["5029"], str(usermasterid)
                        )

                    except Exception as e:
                        archive_viewer_log.exception(e, exc_info=True)
                        archive_viewer_log.error(
                            debugmessages["debug_messages"]["3014"]
                        )
                else:
                    exceptions(404, "404-K", errormessages["errormessagecode"]["779"])

        else:
            exceptions(404, "404-L", errormessages["errormessagecode"]["778"])
    else:
        exceptions(404, "404-M", errormessages["errormessagecode"]["777"])
