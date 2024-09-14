from datetime import datetime, timezone

from ..common.get_orm_classes import get_orm_classes
from ..common.exceptions import exceptions
from ..common.json_responses import (
    errormessages,
    permissions,
    debugmessages,
    infomessages,
    messages
)
from ..common.log_method import application_logger
from ..common.info_log_method import process_logger
from ..common.get_parent_filepath import read_files_from_parent_dir
from ..common.open_json_file import with_open_read_json_file


# Method to update specific user using "Administrator" role.
async def updatewith_adminrole(user_id, info, user_masterid, db):
    ormclass_dict = get_orm_classes()
    Rolemaster = ormclass_dict["Rolemaster"]
    Userrole = ormclass_dict["Userrole"]
    Usermaster = ormclass_dict["Usermaster"]

    archive_viewer_log = application_logger()
    archive_viewer_log_info = process_logger()

    timestamp = datetime.now(timezone.utc)

    role_name = (
        db.query(Rolemaster.rolename).filter(Rolemaster.id == info.roleId).first()
    )
    
    if role_name is not None:
        roleid = (
            db.query(Rolemaster.id, Rolemaster.rolename)
            .join(Userrole, Rolemaster.id == Userrole.rolemasterid)
            .join(Usermaster, Usermaster.id == Userrole.usermasterid)
            .filter(Userrole.usermasterid == user_masterid)
            .first()
        )

        if roleid is not None:
            if role_name.rolename == permissions["roles"]["501"]:
                exceptions(404, "404-I", errormessages["errormessagecode"]["753"])
            elif roleid.rolename == permissions["roles"]["501"]:
                exceptions(404, "404-I", errormessages["errormessagecode"]["752"])

        else:
            archive_viewer_log.error(debugmessages["debug_messages"]["3008"])
            exceptions(404, None, errormessages["errormessagecode"]["723"])

    else:
        exceptions(404, "404-C", errormessages["errormessagecode"]["749"])
    
    if int(user_masterid) == int(user_id):
        
        try:
            if properties["auth_type"] ==  messages["messagecode"]["151"]:
                db.query(Usermaster).filter(Usermaster.id == user_masterid).update(
                    {
                        Usermaster.fullname: info.name,
                        Usermaster.useremail: info.email,
                        Usermaster.last_updated: timestamp,
                        Usermaster.last_updated_by: user_id,
                    }
                )
                db.commit()
                archive_viewer_log_info.info(
                    infomessages["info_messages"]["5029"], str(user_masterid)
                )
        except Exception as e:
            archive_viewer_log.exception(e, exc_info=True)
            archive_viewer_log.error(debugmessages["debug_messages"]["3010"])

    else:
        
        try:
            fileName = read_files_from_parent_dir(3)
            properties = with_open_read_json_file(fileName)
            if properties["auth_type"] ==  messages["messagecode"]["151"]:
                db.query(Usermaster).filter(Usermaster.id == user_masterid).update(
                    {
                        Usermaster.fullname: info.name,
                        Usermaster.useremail: info.email,
                        Usermaster.last_updated: timestamp,
                        Usermaster.last_updated_by: user_id,
                    }
                )

                db.query(Userrole).filter(Userrole.usermasterid == user_masterid).update(
                    {
                        Userrole.rolemasterid: info.roleId,
                        Userrole.last_updated: timestamp,
                        Userrole.last_updated_by: user_id,
                    }
                )
                db.commit()

                archive_viewer_log_info.info(
                    infomessages["info_messages"]["5029"], str(user_masterid)
                )
                
            elif properties["auth_type"] == messages["messagecode"]["150"]:
                
                db.query(Usermaster).filter(Usermaster.id == user_masterid).update(
                    {
                        Usermaster.last_updated: timestamp,
                        Usermaster.last_updated_by: user_id,
                    }
                )

                db.query(Userrole).filter(Userrole.usermasterid == user_masterid).update(
                    {
                        Userrole.rolemasterid: info.roleId,
                        Userrole.last_updated: timestamp,
                        Userrole.last_updated_by: user_id,
                    }
                )
                db.commit()

                archive_viewer_log_info.info(
                    infomessages["info_messages"]["5029"], str(user_masterid)
                )
                
                
        except Exception as e:
            archive_viewer_log.exception(e, exc_info=True)
            archive_viewer_log.error(debugmessages["debug_messages"]["3011"])
