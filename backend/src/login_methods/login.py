import base64
import json
import logging

from datetime import datetime, timezone, timedelta
from pathlib import Path
from sqlalchemy import func

from ..common.exceptions import exceptions
from ..common.get_orm_classes import get_orm_classes
from ..common.info_log_method import process_logger
from ..common.json_responses import (
    debugmessages,
    errormessages,
    infomessages,
    messages,
)
from ..common.log_method import application_logger, setup_logger
from ..common.get_parent_filepath import read_files_from_parent_dir
# from ldap3 import SAFE_SYNC, Connection, Server
# from ldap3.core.exceptions import (
#     LDAPBindError,
#     LDAPException,
#     LDAPExceptionError,
#     LDAPSocketOpenError,
# )

from .authentication import Auth
from .insert_data import insert_data
from .user_lock import update_count
from ..common.open_json_file import with_open_read_json_file

auth_handler = Auth()


# Method to validate the user and return the access token.
async def user_login(response, user_details, db):
    ormclass_dict = get_orm_classes()
    Usermaster = ormclass_dict["Usermaster"]
    Rolemaster = ormclass_dict["Rolemaster"]
    Userrole = ormclass_dict["Userrole"]

    archive_viewer_log_info = process_logger()

    archive_viewer_log = application_logger()

    timestamp = datetime.now(timezone.utc)

    fileName = read_files_from_parent_dir(3)
    maxAge = datetime.now() + timedelta(days=0, minutes=30)

    properties = with_open_read_json_file(fileName)

    login_type = properties["auth_type"]
    createTableStatus = properties["tables_created"]

    if createTableStatus == True:
        # Login using LDAP authentication.
        # if login_type.upper() == messages["messagecode"]["150"]:
        #     qualified_username = (
        #         db.query(Usermaster.fullname)
        #         .filter(Usermaster.username == user_details.username)
        #         .first()
        #     )

        #     if qualified_username is not None:
        #         ldap_username = qualified_username.fullname
        #     else:
        #         ldap_username = user_details.username

        #     use_sslattr = properties["ldapconfig"]["use_ssl"]
        #     if use_sslattr == True or use_sslattr == False:
        #         server = Server(
        #             host=properties["ldapconfig"]["dnsIp"],
        #             port=properties["ldapconfig"]["port"],
        #             use_ssl=use_sslattr,
        #             get_info=properties["ldapconfig"]["get_info"],
        #         )

        #         # Connceting to LDAP server.
        #         try:
        #             Connection(
        #                 server=server,
        #                 authentication=properties["ldapconfig"]["authentication"],
        #                 user=ldap_username,
        #                 password=user_details.psswrd,
        #                 read_only=properties["ldapconfig"]["read_only"],
        #                 client_strategy=SAFE_SYNC,
        #                 auto_bind=True,
        #             )

        #         except LDAPSocketOpenError as e:
        #             archive_viewer_log.exception(e, exc_info=True)
        #             exceptions(503, "503-A", str(e))

        #         except LDAPBindError as e:
        #             archive_viewer_log.exception(e, exc_info=True)
        #             exceptions(409, "409-D", str(e))

        #         except LDAPExceptionError as e:
        #             archive_viewer_log.exception(e, exc_info=True)
        #             exceptions(409, "409-C", str(e))

        #         except LDAPException as e:
        #             archive_viewer_log.exception(e, exc_info=True)
        #             exceptions(409, "409-C", str(e))

        #         except Exception as e:
        #             archive_viewer_log.exception(e, exc_info=True)
        #             exceptions(409, "409-C", str(e))

        #         input_user_name = user_details.username
        #         input_user_name = input_user_name.lower()

        #         user_data = (
        #             db.query(Usermaster.id, Usermaster.active, Usermaster.last_login)
        #             .filter(func.lower(Usermaster.username) == input_user_name)
        #             .first()
        #         )

        #         if user_data is None:
        #             exceptions(409, "409-F", errormessages["errormessagecode"]["920"])

        #         else:
        #             last_login_details = user_data.last_login

        #             # Creating user token for "new-user".
        #             if user_data.active == messages["messagecode"]["114"]:
        #                 try:
        #                     db.query(Usermaster).filter(
        #                         Usermaster.id == user_data.id
        #                     ).update(
        #                         {
        #                             Usermaster.active: messages["messagecode"]["115"],
        #                             Usermaster.last_login: timestamp,
        #                         }
        #                     )
        #                     db.commit()
        #                 except Exception as e:
        #                     archive_viewer_log.exception(e, exc_info=True)
        #                     archive_viewer_log.error(
        #                         debugmessages["debug_messages"]["2059"]
        #                     )

        #                 access_token = auth_handler.encode_token(str(user_data.id))
        #                 response.set_cookie(
        #                     key="access_token",
        #                     value=access_token,
        #                     httponly=True,
        #                     max_age=maxAge,
        #                 )
        #                 insert_data(access_token)
        #                 archive_viewer_log_info.info(
        #                     infomessages["info_messages"]["5040"], user_details.username
        #                 )

        #                 return access_token, last_login_details

        #             # Creating user token for "active" user.
        #             else:
        #                 access_token = auth_handler.encode_token(str(user_data.id))
        #                 db.query(Usermaster).filter(
        #                     Usermaster.id == user_data.id
        #                 ).update({Usermaster.last_login: timestamp})
        #                 db.commit()
        #                 response.set_cookie(
        #                     key="access_token",
        #                     value=access_token,
        #                     httponly=True,
        #                     max_age=maxAge,
        #                 )
        #                 insert_data(access_token)
        #                 archive_viewer_log_info.info(
        #                     infomessages["info_messages"]["5040"], user_details.username
        #                 )

        #                 return access_token, last_login_details
        #     else:
        #         exceptions(409, "409-G", errormessages["errormessagecode"]["794"])

        # Login using BASIC authentication.
        # else:
            input_username = user_details.username
            username = input_username.lower()

            status = (
                db.query(Usermaster.active)
                .filter(Usermaster.username == username)
                .first()
            )

            user_role = (
                db.query(Rolemaster.rolename)
                .join(Userrole, Rolemaster.id == Userrole.rolemasterid)
                .join(Usermaster, Usermaster.id == Userrole.usermasterid)
                .filter(Usermaster.username == username)
                .first()
            )

            if status is None:
                exceptions(401, None, errormessages["errormessagecode"]["702"])

            # Generating temp psswrd for "new-user"..
            elif status.active == messages["messagecode"]["114"]:
                newuser_psswrd = (
                    db.query(Usermaster.psswrd)
                    .filter(
                        Usermaster.username == username,
                        Usermaster.active == messages["messagecode"]["114"],
                        Usermaster.salt == None,
                    )
                    .first()
                )

                if newuser_psswrd is None:
                    exceptions(401, None, errormessages["errormessagecode"]["767"])
                else:
                    base64_message = newuser_psswrd.psswrd
                    base64_bytes = base64_message.encode("ascii")
                    message_bytes = base64.b64decode(base64_bytes)
                    temp_psswrd = message_bytes.decode("ascii")

                    if temp_psswrd == user_details.psswrd:
                        exceptions(
                            404, "404-A", errormessages["errormessagecode"]["810"]
                        )
                    else:
                        # Updating wrong psswrd count in usermaster table.
                        update_count(username, user_role.rolename, db)
                        exceptions(401, None, errormessages["errormessagecode"]["702"])

            elif (
                status.active == messages["messagecode"]["171"]
                and user_role.rolename != messages["messagecode"]["152"]
            ):
                exceptions(404, "404-B", errormessages["errormessagecode"]["814"])
            elif (
                status.active == messages["messagecode"]["172"]
                and user_role.rolename != messages["messagecode"]["152"]
            ):
                exceptions(404, "404-C", errormessages["errormessagecode"]["815"])
            elif (
                status.active == messages["messagecode"]["171"]
                and user_role.rolename == messages["messagecode"]["152"]
            ):
                exceptions(404, "404-E", errormessages["errormessagecode"]["924"])
            elif (
                status.active == messages["messagecode"]["172"]
                and user_role.rolename == messages["messagecode"]["152"]
            ):
                exceptions(404, "404-D", errormessages["errormessagecode"]["925"])

            # Fetching salt value from database
            dbsalt = (
                db.query(Usermaster.salt)
                .filter(Usermaster.username == username)
                .first()
            )

            if len(username) == 0 or len(user_details.psswrd) == 0:
                exceptions(401, None, errormessages["errormessagecode"]["703"])
            elif dbsalt is None:
                exceptions(401, None, errormessages["errormessagecode"]["702"])
            else:
                # Generating psswrd with user input.
                psswrd = auth_handler.encode_psswrd(user_details.psswrd, dbsalt.salt)

                user_info = (
                    db.query(
                        Usermaster.username,
                        Usermaster.psswrd,
                        Usermaster.id,
                        Usermaster.last_login,
                    )
                    .filter(
                        Usermaster.username == username, Usermaster.psswrd == psswrd
                    )
                    .first()
                )
                # Comparing given username and generated psswrd with database username and psswrd.
                if user_info is None:
                    update_count(username, user_role.rolename, db)
                    exceptions(401, None, errormessages["errormessagecode"]["702"])
                else:
                    user_role = (
                        db.query(Rolemaster.rolename)
                        .join(Userrole, Rolemaster.id == Userrole.rolemasterid)
                        .join(Usermaster, Usermaster.id == Userrole.usermasterid)
                        .filter(Usermaster.id == user_info.id)
                        .first()
                    )

                    today = datetime.now()
                    if user_role[0] == messages["messagecode"]["152"]:
                        archive_viewer_log_info.info(
                            infomessages["info_messages"]["5108"]
                        )
                    else:
                        # Checking the psswrd expiry date.
                        expiry_date = (
                            db.query(Usermaster.psswrd_exp_date)
                            .filter(Usermaster.username == username)
                            .first()
                        )

                        if today >= expiry_date.psswrd_exp_date:
                            exceptions(
                                419, "419-A", errormessages["errormessagecode"]["773"]
                            )

                    cwd = Path(__file__).parents[4]
                    fileName = cwd / properties["error_log_path"]

                    dt_string = today.strftime("%d_%b_%Y")
                    loginInfo = "loginInfo" + "_" + dt_string + ".log"
                    login_info = setup_logger(
                        "logininfo_logger" + str(user_info.id),
                        fileName / loginInfo,
                        logging.INFO,
                    )
                    login_info.info(str(username) + " " + "logged in successfully")
                    id_user = user_info.id

                    try:
                        # Fetching last login details
                        last_login = user_info.last_login
                        # Updating last_login in time for user.
                        db.query(Usermaster).filter(Usermaster.id == id_user).update(
                            {
                                Usermaster.active: messages["messagecode"]["115"],
                                Usermaster.last_login: timestamp,
                                Usermaster.wrong_psswrd_cnt: 0,
                            }
                        )
                        db.commit()
                    except Exception as e:
                        archive_viewer_log.exception(e, exc_info=True)
                        archive_viewer_log.error(
                            debugmessages["debug_messages"]["2060"]
                        )

                    access_token = auth_handler.encode_token(str(id_user))
                    response.set_cookie(
                        key="access_token", value=access_token, httponly=True
                    )
                    insert_data(access_token)
                    archive_viewer_log_info.info(
                        infomessages["info_messages"]["5040"], user_details.username
                    )
                    return access_token, last_login
    else:
        exceptions(419, "419-A", debugmessages["debug_messages"]["1981"])
