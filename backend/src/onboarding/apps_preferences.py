import platform

from fastapi import HTTPException

from ..common.json_responses import errormessages, infomessages, messages
from ..common.get_orm_classes import get_orm_classes
from ..common.json_responses import debugmessages, messages, infomessages
from ..common.log_method import application_logger
from ..common.info_log_method import process_logger
from ..common.get_parent_filepath import read_files_from_parent_dir
from ..common.open_json_file import with_open_read_json_file


# Method to check all the on-boarding details are filled or not.
async def is_application_active(db):
    archive_viewer_log = application_logger()
    try:
        ormclass_dict = get_orm_classes()

        Usermaster = ormclass_dict["Usermaster"]
        Rolemaster = ormclass_dict["Rolemaster"]
        Userrole = ormclass_dict["Userrole"]

        fileName = read_files_from_parent_dir(3)

        properties = with_open_read_json_file(fileName)

        authType = properties["auth_type"]
        # queryServerStatus = properties["skip_query_server"]
        # superSetStatus = properties["skip_superset_url"]
        # attribute = properties["attributes"]
        if len(authType) == 0:
            authType = None
        ostype = platform.system()

        superset = properties["superset_url"]
        if len(superset) == 0:
            superset = None

        # # storage_file_path = get_json_path()
        # try:
        #     storage = with_open_read_json_file(storage_file_path)
        #     if not storage:
        #         raise HTTPException(
        #             status_code=422,
        #             detail={
        #                 "message": errormessages["errormessagecode"]["957"],
        #                 "statusCode": 422,
        #                 "errorCode": "422-A",
        #             },
        #         )
        #     else:
        #         storage_path = True
        # except Exception as e:
        #     storage_path = False
        #     archive_viewer_log.exception(e, exc_info=True)
        #     archive_viewer_log.error(debugmessages["debug_messages"]["1981"])

        # convertservername = db.query(Convertservermaster.servername).first()
        # parquetservername = db.query(Queryservermaster.servername).first()

        # archive_viewer_log_info = process_logger()

        # Checks for LDAP authentication type
        # if authType == messages["messagecode"]["150"]:
        #     main_query = (
        #         db.query(Usermaster)
        #         .join(Userrole, Usermaster.id == Userrole.usermasterid)
        #         .join(Rolemaster, Userrole.rolemasterid == Rolemaster.id)
        #         .filter(
        #             Rolemaster.rolename == messages["messagecode"]["152"],
        #             Usermaster.active != messages["messagecode"]["113"],
        #         )
        #     )
        #     users = main_query.with_entities(Usermaster.username).first()

        #     if storage_path == True:
        #         if queryServerStatus == False and superSetStatus == False:
        #             if (
        #                 properties["ldapconfig"]["dnsIp"]
        #                 and properties["ldapconfig"]["port"]
        #                 and properties["ldapconfig"]["get_info"]
        #                 and properties["ldapconfig"]["authentication"]
        #                 and convertservername is not None
        #                 and parquetservername is not None
        #                 and superset is not None
        #                 and (
        #                     properties["ldapconfig"]["use_ssl"] == True
        #                     or properties["ldapconfig"]["use_ssl"] == False
        #                 )
        #                 and (
        #                     properties["ldapconfig"]["read_only"] == True
        #                     or properties["ldapconfig"]["read_only"] == False
        #                 )
        #             ):
        #                 archive_viewer_log_info.info(
        #                     infomessages["info_messages"]["5056"]
        #                 )
        #                 ldap_value = get_ldap_value(True, authType, ostype, attribute)
        #                 return ldap_value
        #             else:
        #                 archive_viewer_log_info.info(
        #                     infomessages["info_messages"]["5056"]
        #                 )
        #                 ldap_value = get_ldap_value(False, authType, ostype, attribute)
        #                 return ldap_value

        #         elif queryServerStatus == False and superSetStatus == True:
        #             if (
        #                 users is not None
        #                 and convertservername is not None
        #                 and parquetservername is not None
        #                 and superset is None
        #             ):
        #                 archive_viewer_log_info.info(
        #                     infomessages["info_messages"]["5056"]
        #                 )
        #                 ldap_value = get_ldap_value(True, authType, ostype, attribute)
        #                 return ldap_value
        #             else:
        #                 archive_viewer_log_info.info(
        #                     infomessages["info_messages"]["5056"]
        #                 )
        #                 ldap_value = get_ldap_value(False, authType, ostype, attribute)
        #                 return ldap_value

        #         elif queryServerStatus == True and superSetStatus == False:
        #             if (
        #                 users is not None
        #                 and convertservername is not None
        #                 and parquetservername is None
        #                 and superset is not None
        #             ):
        #                 archive_viewer_log_info.info(
        #                     infomessages["info_messages"]["5056"]
        #                 )
        #                 ldap_value = get_ldap_value(True, authType, ostype, attribute)
        #                 return ldap_value
        #             else:
        #                 archive_viewer_log_info.info(
        #                     infomessages["info_messages"]["5056"]
        #                 )
        #                 ldap_value = get_ldap_value(False, authType, ostype, attribute)
        #                 return ldap_value

        #         elif queryServerStatus == True and superSetStatus == True:
        #             if (
        #                 properties["ldapconfig"]["dnsIp"]
        #                 and properties["ldapconfig"]["port"]
        #                 and properties["ldapconfig"]["get_info"]
        #                 and properties["ldapconfig"]["authentication"]
        #                 and convertservername is not None
        #                 and parquetservername is None
        #                 and superset is None
        #                 and (
        #                     properties["ldapconfig"]["use_ssl"] == True
        #                     or properties["ldapconfig"]["use_ssl"] == False
        #                 )
        #                 and (
        #                     properties["ldapconfig"]["read_only"] == True
        #                     or properties["ldapconfig"]["read_only"] == False
        #                 )
        #             ):
        #                 archive_viewer_log_info.info(
        #                     infomessages["info_messages"]["5056"]
        #                 )
        #                 ldap_value = get_ldap_value(True, authType, ostype, attribute)
        #                 return ldap_value
        #             else:
        #                 archive_viewer_log_info.info(
        #                     infomessages["info_messages"]["5056"]
        #                 )
        #                 ldap_value = get_ldap_value(False, authType, ostype, attribute)
        #                 return ldap_value
        #         else:
        #             archive_viewer_log.info(infomessages["info_messages"]["5082"])
        #     else:
        #         archive_viewer_log_info.info(infomessages["info_messages"]["5056"])
        #         ldap_value = get_ldap_value(False, authType, ostype, attribute)
        #         return ldap_value

        # Checks for BASIC authentication type
        if authType == messages["messagecode"]["151"]:
            main_query = (
                db.query(Usermaster)
                .join(Userrole, Usermaster.id == Userrole.usermasterid)
                .join(Rolemaster, Userrole.rolemasterid == Rolemaster.id)
                .filter(
                    Rolemaster.rolename == messages["messagecode"]["152"],
                    Usermaster.active != messages["messagecode"]["113"],
                )
            )

            users = main_query.with_entities(Usermaster.username).first()

        #     if storage_path == True:
        #         if queryServerStatus == False and superSetStatus == False:
        #             if (
        #                 users is not None
        #                 and convertservername is not None
        #                 and parquetservername is not None
        #                 and superset is not None
        #             ):
        #                 archive_viewer_log_info.info(
        #                     infomessages["info_messages"]["5056"]
        #                 )
        #                 basic_value = get_basic_value(True, authType, ostype)

        #                 return basic_value
        #             else:
        #                 archive_viewer_log_info.info(
        #                     infomessages["info_messages"]["5056"]
        #                 )
        #                 basic_value = get_basic_value(False, authType, ostype)

        #                 return basic_value

        #         elif queryServerStatus == False and superSetStatus == True:
        #             if (
        #                 users is not None
        #                 and convertservername is not None
        #                 and parquetservername is not None
        #                 and superset is None
        #             ):
        #                 archive_viewer_log_info.info(
        #                     infomessages["info_messages"]["5056"]
        #                 )
        #                 basic_value = get_basic_value(True, authType, ostype)

        #                 return basic_value
        #             else:
        #                 archive_viewer_log_info.info(
        #                     infomessages["info_messages"]["5056"]
        #                 )
        #                 basic_value = get_basic_value(False, authType, ostype)

        #                 return basic_value

        #         elif queryServerStatus == True and superSetStatus == False:
        #             if (
        #                 users is not None
        #                 and convertservername is not None
        #                 and parquetservername is None
        #                 and superset is not None
        #             ):
        #                 archive_viewer_log_info.info(
        #                     infomessages["info_messages"]["5056"]
        #                 )
        #                 basic_value = get_basic_value(True, authType, ostype)

        #                 return basic_value
        #             else:
        #                 archive_viewer_log_info.info(
        #                     infomessages["info_messages"]["5056"]
        #                 )
        #                 basic_value = get_basic_value(False, authType, ostype)

        #                 return basic_value

        #         elif queryServerStatus == True and superSetStatus == True:
        #             if (
        #                 users is not None
        #                 and convertservername is not None
        #                 and parquetservername is None
        #                 and superset is None
        #             ):
        #                 archive_viewer_log_info.info(
        #                     infomessages["info_messages"]["5056"]
        #                 )
        #                 basic_value = get_basic_value(True, authType, ostype)

        #                 return basic_value
        #             else:
        #                 archive_viewer_log_info.info(
        #                     infomessages["info_messages"]["5056"]
        #                 )
        #                 basic_value = get_basic_value(False, authType, ostype)

        #                 return basic_value
        #         else:
        #             archive_viewer_log.info(infomessages["info_messages"]["5082"])
        #     else:
        #         archive_viewer_log_info.info(infomessages["info_messages"]["5056"])
        #         basic_value = get_basic_value(False, authType, ostype)

        #         return basic_value
        # else:
        #     archive_viewer_log_info.info(infomessages["info_messages"]["5056"])
        #     basic_value = get_basic_value(False, authType, ostype)

        #     return basic_value
    
    except KeyError as e:
        archive_viewer_log.error(f"KeyError: Missing key {str(e)} in properties.json file")
        raise HTTPException(
            status_code=400,
            detail={
                "message": f"Missing key: {str(e)} in properties.json file",
                "statusCode": 400,
                "errorCode": "400-B",
            },
        )
    except Exception as e:
        archive_viewer_log.exception(e, exc_info=True)
        archive_viewer_log.error(debugmessages["debug_messages"]["1979"])


# def get_ldap_value(apppreference, authType, ostype, attribute):
#     ldap_value = {"active": "", "authType": "", "platform": "", "attribute": ""}
#     ldap_value["active"] = apppreference
#     ldap_value["authType"] = authType
#     ldap_value["platform"] = ostype
#     ldap_value["attribute"] = attribute
#     return ldap_value


def get_basic_value(apppreference, authType, ostype):
    basic_value = {"active": "", "authType": "", "platform": ""}
    basic_value["active"] = apppreference
    basic_value["authType"] = authType
    basic_value["platform"] = ostype

    return basic_value
