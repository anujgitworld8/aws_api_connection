from ..common.get_orm_classes import get_orm_classes
from ..common.exceptions import exceptions
from ..common.json_responses import errormessages, permissions,messages
from ..roles.check_role import check_role
from ..roles.check_superrole import superrole
from ..roles.check_adminrole import adminrole
from ..common.get_parent_filepath import read_files_from_parent_dir
from ..common.open_json_file import with_open_read_json_file


# Method to create new user.
async def user_create(item, user_id, db):
    ormclass_dict = get_orm_classes()
    Usermaster = ormclass_dict["Usermaster"]

    if not item.roleId:
        exceptions(404, None, errormessages["errormessagecode"]["724"])
    
    username = (
        db.query(Usermaster.username)
        .filter(Usermaster.username == item.username.lower())
        .first()
    )
    useremail = (
        db.query(Usermaster.useremail)
        .filter(Usermaster.useremail == item.email)
        .first()
    )

    if username is None:
        if useremail is not None:
            exceptions(409, "409-A", errormessages["errormessagecode"]["766"])
        else:
            fileName = read_files_from_parent_dir(3)
            properties = with_open_read_json_file(fileName)
            if properties["auth_type"] == messages["messagecode"]["151"]:
                role = await check_role(user_id, db)
                if role == permissions["roles"]["501"]:
                    await superrole(user_id, item, db)

                elif role == permissions["roles"]["502"]:
                    await adminrole(user_id, item, db)

                return item
            else:
                exceptions(409, "409-B", errormessages["errormessagecode"]["1032"])

    else:
        exceptions(409, "409-B", errormessages["errormessagecode"]["725"])
