from ..common.get_orm_classes import get_orm_classes
from ..common.json_responses import messages, debugmessages, infomessages
from ..common.log_method import application_logger
from ..common.info_log_method import process_logger


# Method to insert "Super User" role.
async def insert_superuser(db):
    archive_viewer_log = application_logger()
    try:
        archive_viewer_log_info = process_logger()
        ormclass_dict = get_orm_classes()

        Rolemaster = ormclass_dict["Rolemaster"]

        super_admin_role = (
            db.query(Rolemaster.id)
            .filter(Rolemaster.rolename == messages["messagecode"]["152"])
            .first()
        )
        if super_admin_role is None:
            super_admin_permission = """{
                        "convert":
                            {
                                "write": false,
                                "read": false
                            },
                        "monitor": 
                            {
                                "read": false
                            },
                        "reports":
                            {
                                "read": false
                            },
                        "manageConnections":
                            {
                                "read": true,
                                "write": true,
                                "update": true,
                                "delete": true
                            },
                        "manageUsers":
                            {
                                "read": true,
                                "write": true,
                                "update": true,
                                "delete": true
                            },
                        "utilities":
                            {
                                "read": false,
                                "write": false,
                                "update": false,
                                "delete": false
                            },
                        "applicationSettings":
                            {
                                "read": true,
                                "write": true,
                                "update": true,
                                "delete": true
                            }
                    }"""

            role_info3 = Rolemaster(
                rolename=messages["messagecode"]["152"],
                permission=super_admin_permission,
            )
            db.add(role_info3)
            db.commit()
            db.refresh(role_info3)
            archive_viewer_log_info.info(infomessages["info_messages"]["5009"])
        else:
            archive_viewer_log.error(debugmessages["debug_messages"]["3237"])

    except Exception as e:
        archive_viewer_log.exception(e, exc_info=True)
        archive_viewer_log.error(debugmessages["debug_messages"]["1987"])
