from ..common.get_orm_classes import get_orm_classes
from ..common.json_responses import messages, debugmessages, infomessages
from ..common.log_method import application_logger
from ..common.info_log_method import process_logger


# Method to insert "Administrator" role.
async def insert_admin(db):
    archive_viewer_log = application_logger()
    try:
        archive_viewer_log_info = process_logger()
        ormclass_dict = get_orm_classes()

        Rolemaster = ormclass_dict["Rolemaster"]

        admin_role = (
            db.query(Rolemaster.id)
            .filter(Rolemaster.rolename == messages["messagecode"]["155"])
            .first()
        )
        if admin_role is None:
            admin_permission = """{   
                        "convert":
                            {
                                "write": true,
                                "read": true
                            },
                        "monitor": 
                            {
                                "read": true
                            },
                        "reports":
                            {
                                "read": true
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
                                "read": true,
                                "write": true,
                                "update": true,
                                "delete": true
                            },
                        "applicationSettings":
                            {
                                "read": true,
                                "write": true,
                                "update": true,
                                "delete": true
                            }
                        
                    }"""
            role_info = Rolemaster(
                rolename=messages["messagecode"]["155"], permission=admin_permission
            )
            db.add(role_info)
            db.commit()
            db.refresh(role_info)
            archive_viewer_log_info.info(infomessages["info_messages"]["5005"])

        else:
            archive_viewer_log.error(debugmessages["debug_messages"]["3237"])

    except Exception as e:
        archive_viewer_log.exception(e, exc_info=True)
        archive_viewer_log.error(debugmessages["debug_messages"]["1983"])
