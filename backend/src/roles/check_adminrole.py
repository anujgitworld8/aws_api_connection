from ..common.get_orm_classes import get_orm_classes
from ..common.exceptions import exceptions
from ..common.json_responses import permissions, errormessages

from .insert_userdetails import insert_userdetails
from .insert_userrole import insert_userroles

# Method to create a new user using "Administrator" role.
async def adminrole(user_id, item, db):
    ormclass_dict = get_orm_classes()
    Rolemaster = ormclass_dict["Rolemaster"]

    roleId = item.roleId

    fetch_rolename = (
        db.query(Rolemaster.rolename).filter(Rolemaster.id == item.roleId).first()
    )
    
    if fetch_rolename is not None:
        if fetch_rolename.rolename == permissions["roles"]["501"]:
            exceptions(404, "404-B", errormessages["errormessagecode"]["750"])

        else:
            usermasterid = await insert_userdetails(item, user_id, db)
            await insert_userroles(usermasterid, roleId, user_id, db)
            
    else:
        exceptions(404, "404-C", errormessages["errormessagecode"]["749"])
