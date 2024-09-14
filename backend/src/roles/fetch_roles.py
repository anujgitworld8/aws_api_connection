from src.common.get_orm_classes import get_orm_classes
from src.common.json_responses import debugmessages, permissions, infomessages
from src.common.log_method import application_logger
from src.common.info_log_method import process_logger

from .check_role import check_role


# Method to get the roles based on logged-in user permission.
async def fetch_role(user_id, db):
    archive_viewer_log = application_logger()
    try:
        archive_viewer_log_info = process_logger()
        ormclass_dict = get_orm_classes()
        Rolemaster = ormclass_dict["Rolemaster"]

        response_list = []
        data = db.query(Rolemaster.id, Rolemaster.rolename).all()

        role = await check_role(user_id, db)

        archive_viewer_log_info.info(infomessages["info_messages"]["5032"])

        if role == permissions["roles"]["501"]:
            for i in data:
                if i.rolename == permissions["roles"]["502"]:
                    response_list.append({"id": i.id, "name": i.rolename})
                else:
                    archive_viewer_log_info.info(infomessages["info_messages"]["5093"])

        elif role == permissions["roles"]["502"]:
            for i in data:
                if i.rolename == permissions["roles"]["501"]:
                    archive_viewer_log_info.info(infomessages["info_messages"]["5093"])
                else:
                    response_list.append({"id": i.id, "name": i.rolename})
        else:
            archive_viewer_log_info.info(infomessages["info_messages"]["5093"])

        return response_list
    except Exception as e:
        archive_viewer_log.exception(e, exc_info=True)
        archive_viewer_log.error(debugmessages["debug_messages"]["1964"])
