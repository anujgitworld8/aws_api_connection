from datetime import datetime, timezone, timedelta

from ..common.get_orm_classes import get_orm_classes
from ..common.exceptions import exceptions
from ..common.create_jsonfile import write_logintype

from ..common.json_responses import (
    errormessages,
    messages,
    debugmessages,
    infomessages,
)
from ..users.psswrd_hash import hashpsswrd
from ..login_methods.authentication import Auth
from ..common.log_method import application_logger
from ..common.info_log_method import process_logger
from ..common.get_parent_filepath import read_files_from_parent_dir
from ..common.open_json_file import with_open_read_json_file

auth_handler = Auth()

# Method to create a basic user and return an access token.
async def onboard_createuser(userinfo, db, response):
    ormclass_dict = get_orm_classes()

    Usermaster = ormclass_dict["Usermaster"]
    Rolemaster = ormclass_dict["Rolemaster"]
    Userrole = ormclass_dict["Userrole"]

    archive_viewer_log_info = process_logger()
    archive_viewer_log = application_logger()

    user_name = userinfo.username.lower()
    timestamp = datetime.now(timezone.utc)
    maxAge = datetime.now() + timedelta(minutes=30)
    fileName = read_files_from_parent_dir(3)
    properties = with_open_read_json_file(fileName)
    createTableStatus = properties["tables_created"]

    if createTableStatus:
        if userinfo.loginType.upper() == messages["messagecode"]["151"]:
            usermail_basic = (
                db.query(Usermaster.useremail)
                .filter(Usermaster.useremail == userinfo.email)
                .first()
            )
            username_basic = (
                db.query(Usermaster.id)
                .filter(Usermaster.username == user_name)
                .first()
            )

            if username_basic is not None:
                exceptions(409, "409-B", errormessages["errormessagecode"]["725"])
            elif usermail_basic is not None:
                exceptions(409, "409-A", errormessages["errormessagecode"]["766"])
            else:
                role_id = (
                    db.query(Rolemaster.id)
                    .filter(Rolemaster.rolename == messages["messagecode"]["152"])
                    .first()
                )

                # Create "Super User" if not present.
                hashedpsswrd, salt = hashpsswrd(userinfo.psswrd)
                try:
                    user_details = Usermaster(
                        fullname=userinfo.fullname,
                        username=user_name,
                        psswrd=hashedpsswrd,
                        useremail=userinfo.email,
                        active=messages["messagecode"]["115"],
                        salt=salt,
                        last_updated=timestamp,
                        last_login=None,
                        wrong_psswrd_cnt=0,
                    )
                    db.add(user_details)
                    db.commit()
                    db.refresh(user_details)
                except Exception as e:
                    archive_viewer_log.exception(e, exc_info=True)
                    archive_viewer_log.error(debugmessages["debug_messages"]["2088"])

                userid = user_details.id

                try:
                    role_info = Userrole(
                        usermasterid=userid,
                        rolemasterid=role_id.id,
                        createdate=timestamp,
                        created_by=userid,
                        last_updated=timestamp,
                        last_updated_by=userid,
                    )
                    db.add(role_info)
                    db.commit()
                    db.refresh(role_info)
                except Exception as e:
                    archive_viewer_log.exception(e, exc_info=True)
                    archive_viewer_log.error(debugmessages["debug_messages"]["2089"])

                await write_logintype(userinfo.loginType.upper())
                access_token = auth_handler.encode_token(str(userid))
                archive_viewer_log_info.info(
                    infomessages["info_messages"]["5002"], user_name
                )
                response.set_cookie(
                    key="access_token",
                    value=access_token,
                    httponly=True,
                    max_age=maxAge,
                )
                return access_token
        else:
            exceptions(422, None, errormessages["errormessagecode"]["765"])
    else:
        exceptions(422, None, errormessages["errormessagecode"]["800"])
