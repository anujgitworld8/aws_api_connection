import json

from pathlib import Path

from .log_method import application_logger
from .json_responses import debugmessages
from ..common.get_parent_filepath import read_files_from_parent_dir
from ..common.open_json_file import with_open_read_json_file

filepath = read_files_from_parent_dir(3)


# async def write_ldapconfiguration(new_data, filename=filepath):
#     """Method to update LDAP details in properties.json file."""

#     archive_viewer_log = application_logger()
#     try:
#         file_data = with_open_read_json_file(filename)
#         with open(filename, "r+", encoding="utf-8") as file:
#             file_data = json.load(file)
#             file_data["ldapconfig"].update(new_data)
#             file.seek(0)
#             file.truncate()
#             json.dump(file_data, file, ensure_ascii=False, indent=4)
#     except Exception as e:
#         archive_viewer_log.exception(e, exc_info=True)
#         archive_viewer_log.error(debugmessages["debug_messages"]["1990"])


async def write_logintype(new_data, filename=filepath):
    """Method to update auth type in properties.json file."""

    archive_viewer_log = application_logger()
    try:
        with open(filename, "r+", encoding="utf-8") as file:
            file_data = json.load(file)
            file_data["auth_type"] = new_data
            file.seek(0)
            file.truncate()
            json.dump(file_data, file, ensure_ascii=False, indent=4)
    except Exception as e:
        archive_viewer_log.exception(e, exc_info=True)
        archive_viewer_log.error(debugmessages["debug_messages"]["1991"])


async def store_superseturl(new_data, filename=filepath):
    """Method to update superset_url status in properties.json file."""

    archive_viewer_log = application_logger()
    try:
        with open(filename, "r+", encoding="utf-8") as file:
            file_data = json.load(file)
            new_data = str(new_data)
            file_data["superset_url"] = new_data
            file.seek(0)
            file.truncate()
            json.dump(file_data, file, ensure_ascii=False, indent=4)
    except Exception as e:
        archive_viewer_log.exception(e, exc_info=True)
        archive_viewer_log.error(debugmessages["debug_messages"]["1992"])


async def store_skip_superseturl(new_data, filename=filepath):
    """Method to update skip_superseturl status in properties.json file."""

    archive_viewer_log = application_logger()
    try:
        with open(filename, "r+", encoding="utf-8") as file:
            file_data = json.load(file)
            file_data["skip_superset_url"] = new_data
            file.seek(0)
            file.truncate()
            json.dump(file_data, file, ensure_ascii=False, indent=4)
    except Exception as e:
        archive_viewer_log.exception(e, exc_info=True)
        archive_viewer_log.error(debugmessages["debug_messages"]["1993"])


async def tables_created_status(new_data, filename=filepath):
    """Method to update table_creation status in properties.json file"""

    archive_viewer_log = application_logger()
    try:
        with open(filename, "r+", encoding="utf-8") as file:
            file_data = json.load(file)
            file_data["tables_created"] = new_data
            file.seek(0)
            file.truncate()
            json.dump(file_data, file, ensure_ascii=False, indent=4)
    except Exception as e:
        archive_viewer_log.exception(e, exc_info=True)
        archive_viewer_log.error(debugmessages["debug_messages"]["1994"])


async def metadata_configuration(new_data, filename=filepath):
    """Method to update metadata configuration in properties.json file"""

    archive_viewer_log = application_logger()
    try:
        with open(filename, "r+", encoding="utf-8") as file:
            file_data = json.load(file)
            file_data["metadata_config"] = new_data
            file.seek(0)
            file.truncate()
            json.dump(file_data, file, ensure_ascii=False, indent=4)
    except Exception as e:
        archive_viewer_log.exception(e, exc_info=True)
        archive_viewer_log.error(debugmessages["debug_messages"]["1995"])


# async def update_queryserver_flag(new_data, filename=filepath):
#     """Method to update query server skip flag in properties.json file"""

#     archive_viewer_log = application_logger()
#     try:
#         with open(filename, "r+", encoding="utf-8") as file:
#             file_data = json.load(file)
#             file_data["skip_query_server"] = new_data
#             file.seek(0)
#             file.truncate()
#             json.dump(file_data, file, ensure_ascii=False, indent=4)
#     except Exception as e:
#         archive_viewer_log.exception(e, exc_info=True)
#         archive_viewer_log.error(debugmessages["debug_messages"]["3234"])


# async def update_queryserver_ssl(new_data, filename=filepath):
#     """Method to update query server ssl value in properties.json file"""

#     archive_viewer_log = application_logger()
#     try:
#         with open(filename, "r+", encoding="utf-8") as file:
#             file_data = json.load(file)
#             file_data["queryserver"]["use_ssl"] = new_data
#             file.seek(0)
#             file.truncate()
#             json.dump(file_data, file, ensure_ascii=False, indent=4)
#     except Exception as e:
#         archive_viewer_log.exception(e, exc_info=True)
#         archive_viewer_log.error(debugmessages["debug_messages"]["2012"])


# async def update_ldap_search_filter(new_data, filename=filepath):
#     """Method to update ldap search filter value in properties.json file"""

#     archive_viewer_log = application_logger()
#     try:
#         with open(filename, "r+", encoding="utf-8") as file:
#             file_data = json.load(file)
#             file_data["ldap_search_filter"] = new_data
#             file.seek(0)
#             file.truncate()
#             json.dump(file_data, file, ensure_ascii=False, indent=4)
#     except Exception as e:
#         archive_viewer_log.exception(e, exc_info=True)
#         archive_viewer_log.error(debugmessages["debug_messages"]["2012"])


async def update_attributes(new_data, filename=filepath):
    """Method to update attributes value in properties.json file"""

    archive_viewer_log = application_logger()
    try:
        with open(filename, "r+", encoding="utf-8") as file:
            file_data = json.load(file)
            file_data["attributes"] = new_data
            file.seek(0)
            file.truncate()
            json.dump(file_data, file, ensure_ascii=False, indent=4)
    except Exception as e:
        archive_viewer_log.exception(e, exc_info=True)
        archive_viewer_log.error(debugmessages["debug_messages"]["2012"])
