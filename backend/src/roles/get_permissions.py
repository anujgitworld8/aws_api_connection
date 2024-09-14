import json

from ..common.get_orm_classes import get_orm_classes
from ..common.json_responses import errormessages, debugmessages
from ..common.exceptions import exceptions
from ..common.log_method import application_logger


# Method to fetch the role and permission of logged-in user.
def get_permissions(usermaster_id, db):
    try:
        archive_viewer_log = application_logger()

        ormclass_dict = get_orm_classes()
        Rolemaster = ormclass_dict["Rolemaster"]
        Userrole = ormclass_dict["Userrole"]
        Usermaster = ormclass_dict["Usermaster"]

        role_details = (
            db.query(Rolemaster.rolename, Rolemaster.permission)
            .join(Userrole, Rolemaster.id == Userrole.rolemasterid)
            .join(Usermaster, Usermaster.id == Userrole.usermasterid)
            .filter(Userrole.usermasterid == usermaster_id)
            .first()
        )
        if role_details is None:
            exceptions(404, "404-B", errormessages["errormessagecode"]["744"])

        else:
            json_data = json.loads(role_details.permission)
            final_permissions = json_data
            role_name = role_details.rolename

            return role_name, final_permissions

    except Exception as e:
        archive_viewer_log.exception(e, exc_info=True)
        archive_viewer_log.error(debugmessages["debug_messages"]["3008"])
