from ..common.log_method import application_logger
from ..common.get_orm_classes import get_orm_classes
from ..roles.check_role import check_role
from ..roles.get_response_list import get_response_list
from ..common.json_responses import (
    errormessages,
    messages,
    permissions,
    debugmessages,
)
from ..common.exceptions import exceptions

from .specific_userdelete import delete_specificuser


# Method to delete specific user.
async def user_delete(userId, user_id, db):
    ormclass_dict = get_orm_classes()
    Rolemaster = ormclass_dict["Rolemaster"]
    Userrole = ormclass_dict["Userrole"]
    Usermaster = ormclass_dict["Usermaster"]

    archive_viewer_log = application_logger()

    if user_id == userId:
        exceptions(404, "404-N", errormessages["errormessagecode"]["726"])
    else:
        userdetails = (
            db.query(Usermaster.active, Usermaster.username, Usermaster.useremail)
            .filter(Usermaster.id == userId)
            .first()
        )

        if userdetails is None:
            exceptions(404, "404-O", errormessages["errormessagecode"]["723"])
        elif userdetails.active == messages["messagecode"]["113"]:
            exceptions(404, "404-P", errormessages["errormessagecode"]["761"])
        else:
            usermail = userdetails.useremail
            username = userdetails.username

            role_result = (
                db.query(Rolemaster.rolename)
                .join(Userrole, Rolemaster.id == Userrole.rolemasterid)
                .join(Usermaster, Usermaster.id == Userrole.usermasterid)
                .filter(Usermaster.id == userId)
                .all()
            )

            archive_viewer_log.error(debugmessages["debug_messages"]["3020"])

            userrole_list = await get_response_list(role_result)

            loggedin_userrole = await check_role(user_id, db)

            if loggedin_userrole == permissions["roles"]["501"]:
                if permissions["roles"]["502"] in userrole_list:
                    await delete_specificuser(usermail, username, user_id, userId, db)
                    return messages["returnmessagecode"]["617"]
                else:
                    exceptions(404, "404-Q", errormessages["errormessagecode"]["727"])

            elif loggedin_userrole == permissions["roles"]["502"]:
                if permissions["roles"]["501"] in userrole_list:
                    exceptions(404, "404-R", errormessages["errormessagecode"]["728"])
                else:
                    await delete_specificuser(usermail, username, user_id, userId, db)
                    return messages["returnmessagecode"]["617"]
