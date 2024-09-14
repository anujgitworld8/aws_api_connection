from ..common.get_orm_classes import get_orm_classes
from ..common.json_responses import errormessages, permissions, debugmessages
from ..common.exceptions import exceptions
from ..common.log_method import application_logger

from .insert_userdetails import insert_userdetails
from .insert_userrole import insert_userroles


# Method to create new user using "Super User" role.
async def superrole(user_id, item, db):
    ormclass_dict = get_orm_classes()
    Rolemaster = ormclass_dict["Rolemaster"]

    archive_viewer_log = application_logger()
    roleId = item.roleId

    try:
        userrole = db.query(Rolemaster.rolename).filter(Rolemaster.id == roleId).first()
    except Exception as e:
        archive_viewer_log.exception(e, exc_info=True)
        archive_viewer_log.error(debugmessages["debug_messages"]["3008"])

    if userrole is not None:
        if userrole.rolename == permissions["roles"]["502"]:
            usermasterid = await insert_userdetails(item, user_id, db)
            await insert_userroles(usermasterid, roleId, user_id, db)

        else:
            exceptions(404, "404-D", errormessages["errormessagecode"]["748"])
    else:
        exceptions(404, "404-E", errormessages["errormessagecode"]["749"])
