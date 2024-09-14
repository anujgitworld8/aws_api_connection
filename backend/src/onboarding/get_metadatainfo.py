from ..common.log_method import application_logger
from ..common.json_responses import (
    debugmessages,
    messages,
    infomessages,
    errormessages,
)
from ..common.info_log_method import process_logger
from ..common.get_parent_filepath import read_files_from_parent_dir
from ..common.open_json_file import with_open_read_json_file


# Method to return metadata information.
async def getjson_metadata():
    archive_viewer_log = application_logger()
    try:
        archive_viewer_log_info = process_logger()
        response_list = []

        fileName = read_files_from_parent_dir(3)

        properties = with_open_read_json_file(fileName)

        createTableStatus = properties["tables_created"]
        if createTableStatus == True:
            if (
                (
                    properties["metadata_config"]["databaseType"].lower()
                    == messages["messagecode"]["184"]
                )
                or (
                    properties["metadata_config"]["databaseType"].lower()
                    == messages["messagecode"]["187"]
                )
                or (
                    properties["metadata_config"]["databaseType"].lower()
                    == messages["messagecode"]["214"]
                )
            ):
                psswd = properties["metadata_config"]["psswrd"]
                if len(psswd) == 0:
                    archive_viewer_log.error(errormessages["errormessagecode"]["905"])
                else:
                    databaseType = properties["metadata_config"]["databaseType"]
                    host = properties["metadata_config"]["host"]
                    port = properties["metadata_config"]["port"]
                    username = properties["metadata_config"]["username"]
                    databaseName = properties["metadata_config"]["databaseName"]

                    if databaseType and host and port and username and databaseName:
                        response_list.append(
                            {
                                "databaseType": databaseType,
                                "host": host,
                                "port": port,
                                "username": username,
                                "databaseName": databaseName,
                            }
                        )
                    archive_viewer_log_info.info(
                        infomessages["info_messages"]["5004"], databaseType
                    )
                    return response_list

            elif (
                properties["metadata_config"]["databaseType"].lower()
                == messages["messagecode"]["185"]
            ):
                psswd = properties["metadata_config"]["psswrd"]
                if len(psswd) == 0:
                    archive_viewer_log.error(errormessages["errormessagecode"]["905"])
                else:
                    databaseType = properties["metadata_config"]["databaseType"]
                    host = properties["metadata_config"]["host"]
                    port = properties["metadata_config"]["port"]
                    username = properties["metadata_config"]["username"]
                    databaseName = properties["metadata_config"]["databaseName"]
                    connectionType = properties["metadata_config"]["connectionType"]

                    if databaseType and host and port and username and databaseName:
                        response_list.append(
                            {
                                "databaseType": databaseType,
                                "host": host,
                                "port": port,
                                "username": username,
                                "databaseName": databaseName,
                                "connectionType": connectionType,
                            }
                        )
                    archive_viewer_log_info.info(
                        infomessages["info_messages"]["5004"], databaseType
                    )
                    return response_list

            elif (
                properties["metadata_config"]["databaseType"].lower()
                == messages["messagecode"]["186"]
            ):
                databaseType = properties["metadata_config"]["databaseType"]
                host = properties["metadata_config"]["host"]
                port = properties["metadata_config"]["port"]
                username = properties["metadata_config"]["username"]
                databaseName = properties["metadata_config"]["databaseName"]
                loginType = properties["metadata_config"]["loginType"]

                if databaseType and host and port and username and databaseName:
                    response_list.append(
                        {
                            "databaseType": databaseType,
                            "host": host,
                            "port": port,
                            "username": username,
                            "databaseName": databaseName,
                            "loginType": loginType,
                        }
                    )
                    return response_list
                elif databaseType and host and port and databaseName and loginType:
                    response_list.append(
                        {
                            "databaseType": databaseType,
                            "host": host,
                            "port": port,
                            "databaseName": databaseName,
                            "loginType": loginType,
                        }
                    )
                    return response_list

            elif (
                properties["metadata_config"]["databaseType"].lower()
                == messages["messagecode"]["188"]
            ):
                databaseType = properties["metadata_config"]["databaseType"]
                host = properties["metadata_config"]["host"]
                username = properties["metadata_config"]["username"]
                databaseName = properties["metadata_config"]["databaseName"]

                if databaseType and databaseName:
                    response_list.append(
                        {
                            "databaseType": databaseType,
                            "host": host,
                            "username": username,
                            "databaseName": databaseName,
                        }
                    )
                    archive_viewer_log_info.info(
                        infomessages["info_messages"]["5004"], databaseType
                    )
                    return response_list
        else:
            return response_list
    except Exception as e:
        archive_viewer_log.exception(e, exc_info=True)
        archive_viewer_log.error(debugmessages["debug_messages"]["1982"])
