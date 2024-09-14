import json

from pathlib import Path

from ..common.get_orm_classes import get_orm_classes
from ..common.log_method import application_logger
from ..common.json_responses import debugmessages, messages
from ..common.get_parent_filepath import read_files_from_parent_dir
from ..common.open_json_file import with_open_read_json_file


# Method to fetch all the on-boarding details based on the completed steps.
async def get_onboard_details(db, user_id):
    archive_viewer_log = application_logger()
    try:
        ormclass_dict = get_orm_classes()

        # Convertservermaster = ormclass_dict["Convertservermaster"]
        # Queryservermaster = ormclass_dict["Queryservermaster"]
        Usermaster = ormclass_dict["Usermaster"]

        response_list = []
        response_list1 = []
        convert_servers_list = []
        storage_details = []

        fileName = read_files_from_parent_dir(3)
        fileName = str(fileName)
        properties = with_open_read_json_file(fileName)

        # storage_details = get_storage_manager()
        superset_url = properties["superset_url"]

        logintype = properties["auth_type"]
        # logonType = properties["ldapconfig"]["authenticationType"]

        if logintype == "":
            return None

        # Fetch the on-boarding details for BASIC authentication.
        if logintype.upper() == messages["messagecode"]["151"]:
            res = (
                db.query(Usermaster.username, Usermaster.fullname, Usermaster.useremail)
                .filter(
                    Usermaster.id == user_id,
                    Usermaster.active != messages["messagecode"]["113"],
                )
                .first()
            )

            if res is None:
                # returns auth_type only as user details are not found
                response_list.append(
                    {
                        "login_type": logintype,
                        "user_details": None,
                        # "storage_details": None,
                        # "convertserver_details": None,
                        # "queryserver_details": None,
                        "superset_url": None,
                    }
                )
                return response_list
            # else:
            #     basicfullname = res.fullname
            #     basicusername = res.username
            #     basicemail = res.useremail

                # convert_server_details = (
                #     db.query(
                #         Convertservermaster.id,
                #         Convertservermaster.servername,
                #         Convertservermaster.optim_directory,
                #         Convertservermaster.default_qualifier,
                #         Convertservermaster.psthomepath,
                #         Convertservermaster.destination_location,
                #         Convertservermaster.source_location,
                #         Convertservermaster.source_mount_path,
                #         Convertservermaster.destination_mount_path,
                #         Convertservermaster.platform_type,
                #     )
                #     .order_by(Convertservermaster.id)
                #     .all()
                # )

                # if convert_server_details is None:
                #     # returns auth_type and user details as convertserver details are not found
                #     response_list.append(
                #         {
                #             "login_type": logintype,
                #             "user_details": {
                #                 "id": user_id,
                #                 "fullname": basicfullname,
                #                 "username": basicusername,
                #                 "email": basicemail,
                #             },
                #             "storage_details": storage_details,
                #             "convertserver_details": None,
                #             "queryserver_details": None,
                #             "superset_url": None,
                #         }
                #     )
                #     return response_list
                # else:
                #     for row in convert_server_details:
                #         temp = {
                #             "id": row.id,
                #             "optimServerName": row.servername,
                #             "optimDirectory": row.optim_directory,
                #             "defaultQualifier": row.default_qualifier,
                #             "psthomePath": row.psthomepath,
                #             "sourcePath": row.source_location,
                #             "destinationPath": row.destination_location,
                #             "sourceMountPath": row.source_mount_path,
                #             "destinationMountPath": row.destination_mount_path,
                #             "platformType": row.platform_type,
                #         }
                #         convert_servers_list.append(temp)

                    # data = db.query(
                    #     Queryservermaster.id,
                    #     Queryservermaster.servername,
                    #     Queryservermaster.serverip,
                    #     Queryservermaster.httpport,
                    #     Queryservermaster.username,
                    # ).first()

                # if data is None and superset_url != "":
                #     # returns only auth_type, user details, convertserver details and report URL if queryserver details are not found
                #     response_list.append(
                #         {
                #             "login_type": logintype,
                #             "user_details": {
                #                 "id": user_id,
                #                 "fullname": basicfullname,
                #                 "username": basicusername,
                #                 "email": basicemail,
                #             },
                #             # "storage_details": storage_details,
                #             # "convertserver_details": convert_servers_list,
                #             # "queryserver_details": None,
                #             "superset_url": superset_url,
                #         }
                #     )
                #     return response_list
                        # elif data is None and superset_url == "":
                        #     # returns auth_type, user and convertserver details as queryserver details are not found
                        #     response_list.append(
                        #         {
                        #             "login_type": logintype,
                        #             "user_details": {
                        #                 "id": user_id,
                        #                 "fullname": basicfullname,
                        #                 "username": basicusername,
                        #                 "email": basicemail,
                        #             },
                        #             "storage_details": storage_details,
                        #             "convertserver_details": convert_servers_list,
                        #             "queryserver_details": None,
                        #             "superset_url": None,
                        #         }
                        #     )
                        #     return response_list
        #             # else:
        #             #     query_serverid = data.id
        #             #     query_server_name = data.servername
        #             #     query_server_host = data.serverip
        #             #     query_server_port = data.httpport
        #             #     query_server_username = data.username

        #                 if superset_url == "":
        #                     # returns auth_type, user, convertserver and queryserver details as report url is not found
        #                     response_list.append(
        #                         {
        #                             "login_type": logintype,
        #                             "user_details": {
        #                                 "id": user_id,
        #                                 "fullname": basicfullname,
        #                                 "username": basicusername,
        #                                 "email": basicemail,
        #                             },
        #                             "storage_details": storage_details,
        #                             "convertserver_details": convert_servers_list,
        #                             "queryserver_details": {
        #                                 "id": query_serverid,
        #                                 "queryServerName": query_server_name,
        #                                 "host": query_server_host,
        #                                 "port": query_server_port,
        #                                 "username": query_server_username,
        #                                 "ssl": properties["queryserver"]["use_ssl"],
        #                             },
        #                             "superset_url": None,
        #                         }
        #                     )
        #                     return response_list
        #                 else:
        #                     # returns auth_type, user, convertserver, queryserver and superset_url details.
        #                     response_list.append(
        #                         {
        #                             "login_type": logintype,
        #                             "user_details": {
        #                                 "id": user_id,
        #                                 "fullname": basicfullname,
        #                                 "username": basicusername,
        #                                 "email": basicemail,
        #                             },
        #                             "storage_details": storage_details,
        #                             "convertserver_details": convert_servers_list,
        #                             "queryserver_details": {
        #                                 "id": query_serverid,
        #                                 "queryServerName": query_server_name,
        #                                 "host": query_server_host,
        #                                 "port": query_server_port,
        #                                 "username": query_server_username,
        #                                 "ssl": properties["queryserver"]["use_ssl"],
        #                             },
        #                             "superset_url": superset_url,
        #                         }
        #                     )
        #                     return response_list

        # # Fetch the on-boarding details for for LDAP authentication
        # elif logintype.upper() == messages["messagecode"]["150"]:
        #     result = (
        #         db.query(Usermaster.useremail, Usermaster.fullname, Usermaster.username)
        #         .filter(Usermaster.id == user_id)
        #         .first()
        #     )

        #     if result is None:
        #         # returns only auth_type as user details are not found
        #         response_list1.append(
        #             {
        #                 "authenticationType": logonType,
        #                 "login_type": logintype,
        #                 "user_details": None,
        #                 "storage_details": None,
        #                 "convertserver_details": None,
        #                 "queryserver_details": None,
        #                 "superset_url": None,
        #             }
        #         )
        #         return response_list1
        #     else:
        #         ldapuser = user_id
        #         ldap_dnsIp = properties["ldapconfig"]["dnsIp"]
        #         ldapport = properties["ldapconfig"]["port"]
        #         ldapusername = result.fullname
        #         ldapTLS = properties["ldapconfig"]["use_ssl"]
        #         baseDN = properties["ldapconfig"]["baseDN"]

        #         convert_server_details = (
        #             db.query(
        #                 Convertservermaster.id,
        #                 Convertservermaster.servername,
        #                 Convertservermaster.optim_directory,
        #                 Convertservermaster.default_qualifier,
        #                 Convertservermaster.psthomepath,
        #                 Convertservermaster.destination_location,
        #                 Convertservermaster.source_location,
        #                 Convertservermaster.source_mount_path,
        #                 Convertservermaster.destination_mount_path,
        #                 Convertservermaster.platform_type,
        #             )
        #             .order_by(Convertservermaster.id)
        #             .all()
        #         )
        #         if convert_server_details is None:
        #             # returns auth_type and user details as convertserver details are not found.
        #             response_list1.append(
        #                 {
        #                     "login_type": logintype,
        #                     "user_details": {
        #                         "id": ldapuser,
        #                         "ldapHost/Ip": ldap_dnsIp,
        #                         "port": ldapport,
        #                         "username": ldapusername,
        #                         "TLS": ldapTLS,
        #                         "baseDN": baseDN,
        #                         "authenticationType": logonType,
        #                     },
        #                     "storage_details": storage_details,
        #                     "convertserver_details": None,
        #                     "queryserver_details": None,
        #                 }
        #             )
        #             return response_list1
        #         else:
        #             for row in convert_server_details:
        #                 temp = {
        #                     "id": row.id,
        #                     "optimServerName": row.servername,
        #                     "optimDirectory": row.optim_directory,
        #                     "defaultQualifier": row.default_qualifier,
        #                     "psthomePath": row.psthomepath,
        #                     "sourcePath": row.source_location,
        #                     "destinationPath": row.destination_location,
        #                     "sourceMountPath": row.source_mount_path,
        #                     "destinationMountPath": row.destination_mount_path,
        #                     "platformType": row.platform_type,
        #                 }
        #                 convert_servers_list.append(temp)

        #             serverdetails = db.query(
        #                 Queryservermaster.id,
        #                 Queryservermaster.servername,
        #                 Queryservermaster.serverip,
        #                 Queryservermaster.httpport,
        #                 Queryservermaster.username,
        #             ).first()
        #             if serverdetails is None and superset_url != "":
        #                 # returns only auth_type, user details, convertserver details and report URL if queryserver details are not found
        #                 response_list1.append(
        #                     {
        #                         "login_type": logintype,
        #                         "user_details": {
        #                             "id": ldapuser,
        #                             "ldapHost/Ip": ldap_dnsIp,
        #                             "port": ldapport,
        #                             "username": ldapusername,
        #                             "TLS": ldapTLS,
        #                             "baseDN": baseDN,
        #                             "authenticationType": logonType,
        #                         },
        #                         "storage_details": storage_details,
        #                         "convertserver_details": convert_servers_list,
        #                         "queryserver_details": None,
        #                         "superset_url": superset_url,
        #                     }
        #                 )
        #                 return response_list1
        #             elif serverdetails is None and superset_url == "":
        #                 # returns auth_type, user and convertserver details as queryserver details are not found
        #                 response_list1.append(
        #                     {
        #                         "login_type": logintype,
        #                         "user_details": {
        #                             "id": ldapuser,
        #                             "ldapHost/Ip": ldap_dnsIp,
        #                             "port": ldapport,
        #                             "username": ldapusername,
        #                             "TLS": ldapTLS,
        #                             "baseDN": baseDN,
        #                             "authenticationType": logonType,
        #                         },
        #                         "storage_details": storage_details,
        #                         "convertserver_details": convert_servers_list,
        #                         "queryserver_details": None,
        #                         "superset_url": None,
        #                     }
        #                 )
        #                 return response_list1
        #             else:
        #                 queryserver_id = serverdetails.id
        #                 queryserver_name = serverdetails.servername
        #                 queryserver_host = serverdetails.serverip
        #                 queryserver_port = serverdetails.httpport
        #                 queryserver_username = serverdetails.username

        #                 if superset_url == "":
        #                     # returns auth_type, user, convertserver and queryserver details as report url is not found
        #                     response_list1.append(
        #                         {
        #                             "login_type": logintype,
        #                             "user_details": {
        #                                 "id": ldapuser,
        #                                 "ldapHost/Ip": ldap_dnsIp,
        #                                 "port": ldapport,
        #                                 "username": ldapusername,
        #                                 "TLS": ldapTLS,
        #                                 "baseDN": baseDN,
        #                                 "authenticationType": logonType,
        #                             },
        #                             "storage_details": storage_details,
        #                             "convertserver_details": convert_servers_list,
        #                             "queryserver_details": {
        #                                 "id": queryserver_id,
        #                                 "queryServerName": queryserver_name,
        #                                 "host": queryserver_host,
        #                                 "port": queryserver_port,
        #                                 "username": queryserver_username,
        #                                 "ssl": properties["queryserver"]["use_ssl"],
        #                             },
        #                             "superset_url": None,
        #                         }
        #                     )
        #                     return response_list1
        #                 else:
        #                     # returns auth_type, user, convertserver, queryserver and report details.
        #                     response_list1.append(
        #                         {
        #                             "login_type": logintype,
        #                             "user_details": {
        #                                 "id": ldapuser,
        #                                 "ldapHost/Ip": ldap_dnsIp,
        #                                 "port": ldapport,
        #                                 "username": ldapusername,
        #                                 "TLS": ldapTLS,
        #                                 "baseDN": baseDN,
        #                                 "authenticationType": logonType,
        #                             },
        #                             "storage_details": storage_details,
        #                             "convertserver_details": convert_servers_list,
        #                             "queryserver_details": {
        #                                 "id": queryserver_id,
        #                                 "queryServerName": queryserver_name,
        #                                 "host": queryserver_host,
        #                                 "port": queryserver_port,
        #                                 "username": queryserver_username,
        #                                 "ssl": properties["queryserver"]["use_ssl"],
        #                             },
        #                             "superset_url": superset_url,
        #                         }
        #                     )
                            # return response_list1
        else:
            archive_viewer_log.error(debugmessages["debug_messages"]["3236"])

    except Exception as e:
        archive_viewer_log.exception(e, exc_info=True)
        archive_viewer_log.error(debugmessages["debug_messages"]["1981"])
