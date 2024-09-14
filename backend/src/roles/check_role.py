from ..common.get_orm_classes import get_orm_classes
from ..common.json_responses import permissions, debugmessages
from ..common.log_method import application_logger


# Method to check the logged-in user role.
async def check_role(user_id, db):
    archive_viewer_log = application_logger()
    try:
        ormclass_dict = get_orm_classes()
        Rolemaster = ormclass_dict["Rolemaster"]
        Userrole = ormclass_dict["Userrole"]
        Usermaster = ormclass_dict["Usermaster"]

        user_role = (
            db.query(Rolemaster.rolename)
            .join(Userrole, Rolemaster.id == Userrole.rolemasterid)
            .join(Usermaster, Usermaster.id == Userrole.usermasterid)
            .filter(Usermaster.id == user_id)
            .first()
        )

        if user_role is not None:
            if user_role.rolename == permissions["roles"]["501"]:
                return permissions["roles"]["501"]

            elif user_role.rolename == permissions["roles"]["502"]:
                return permissions["roles"]["502"]
            else:
                return None
        else:
            archive_viewer_log.exception(e, exc_info=True)
            archive_viewer_log.error(debugmessages["debug_messages"]["3008"])
            return None
    except Exception as e:
        archive_viewer_log.exception(e, exc_info=True)
        archive_viewer_log.error(debugmessages["debug_messages"]["1962"])
