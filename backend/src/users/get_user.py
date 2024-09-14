from ..roles.check_role import check_role
from ..roles.get_response_list import get_response_list
from ..common.json_responses import messages, errormessages, permissions, infomessages
from ..common.exceptions import exceptions
from ..common.info_log_method import process_logger
from ..common.get_orm_classes import get_orm_classes

from .get_user_data import get_userdata


# Method to get all user details.
async def get_all_users(user_id, db):
    ormclass_dict = get_orm_classes()
    Rolemaster = ormclass_dict["Rolemaster"]
    Userrole = ormclass_dict["Userrole"]
    Usermaster = ormclass_dict["Usermaster"]
    archive_viewer_log_info = process_logger()
    all_usermasterid = (
        db.query(Usermaster.id)
        .filter(Usermaster.active != messages["messagecode"]["113"])
        .all()
    )

    response_list = []
    if all_usermasterid != []:
        role = await check_role(user_id, db)
        for user in all_usermasterid:
            userrole = (
                db.query(Rolemaster.rolename)
                .join(Userrole, Rolemaster.id == Userrole.rolemasterid)
                .join(Usermaster, Userrole.usermasterid == Usermaster.id)
                .filter(Usermaster.id == user.id)
                .all()
            )

            role_list = await get_response_list(userrole)

            if role == permissions["roles"]["502"]:
                if permissions["roles"]["501"] not in role_list:
                    users = (
                        db.query(Usermaster)
                        .join(Userrole, Usermaster.id == Userrole.usermasterid)
                        .join(Rolemaster, Userrole.rolemasterid == Rolemaster.id)
                        .filter(Usermaster.id == user.id)
                    )
                    userdetails = (
                        users.with_entities(
                            Usermaster.id,
                            Usermaster.username,
                            Usermaster.psswrd,
                            Usermaster.active,
                            Usermaster.created_date,
                            Usermaster.created_by,
                            Usermaster.last_updated,
                            Usermaster.last_updated_by,
                            Usermaster.useremail,
                            Usermaster.fullname,
                        )
                        .filter(Usermaster.id == user.id)
                        .first()
                    )

                    archive_viewer_log_info.info(
                        infomessages["info_messages"]["5035"], userdetails.username
                    )

                    userinfo = await get_userdata(userdetails, userrole)
                    if userinfo is not None:
                        response_list.append(userinfo)

            elif role == permissions["roles"]["501"] and (
                permissions["roles"]["501"] in role_list
                or permissions["roles"]["502"] in role_list
            ):
                userdetails = (
                    db.query(
                        Usermaster.id,
                        Usermaster.username,
                        Usermaster.psswrd,
                        Usermaster.active,
                        Usermaster.created_date,
                        Usermaster.created_by,
                        Usermaster.last_updated,
                        Usermaster.last_updated_by,
                        Usermaster.useremail,
                        Usermaster.fullname,
                    )
                    .filter(Usermaster.id == user.id)
                    .first()
                )
                archive_viewer_log_info.info(
                    infomessages["info_messages"]["5035"], userdetails.username
                )

                userinfo = await get_userdata(userdetails, userrole)
                if userinfo is not None:
                    response_list.append(userinfo)
        return response_list
    else:
        exceptions(404, None, errormessages["errormessagecode"]["723"])
