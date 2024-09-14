from ..common.get_orm_classes import get_orm_classes
from ..common.json_responses import errormessages, messages, permissions, infomessages
from ..common.exceptions import exceptions
from ..roles.check_role import check_role
from ..roles.update_superrole import updatewith_superrole
from ..roles.update_adminrole import updatewith_adminrole
from ..roles.get_response_list import get_response_list
from ..common.info_log_method import process_logger


# Method to update specific user details.
async def user_update(usermasterId, info, user_id, db):
    ormclass_dict = get_orm_classes()
    Usermaster = ormclass_dict["Usermaster"]
    archive_viewer_log_info = process_logger()

    usermaster_id = (
        db.query(Usermaster.id).filter(Usermaster.id == usermasterId).first()
    )

    if usermaster_id is None:
        exceptions(404, None, errormessages["errormessagecode"]["723"])
    else:
        status = (
            db.query(Usermaster.active).filter(Usermaster.id == usermasterId).first()
        )
        if status.active == messages["messagecode"]["113"]:
            exceptions(404, None, errormessages["errormessagecode"]["761"])

        alluseremail = (
            db.query(Usermaster.useremail)
            .filter(
                Usermaster.active != messages["messagecode"]["113"],
                Usermaster.id != usermasterId,
            )
            .all()
        )
        useremaillist = await get_response_list(alluseremail)

        if info.email in useremaillist:
            exceptions(409, "409-A", errormessages["errormessagecode"]["766"])
        else:
            role = await check_role(user_id, db)
            if role == permissions["roles"]["501"]:
                await updatewith_superrole(user_id, info, usermasterId, db)

            elif role == permissions["roles"]["502"]:
                await updatewith_adminrole(user_id, info, usermasterId, db)

            else:
                archive_viewer_log_info.info(infomessages["info_messages"]["5093"])
            return messages["returnmessagecode"]["616"]
