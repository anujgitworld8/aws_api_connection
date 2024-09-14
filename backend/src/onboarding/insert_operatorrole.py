from ..common.get_orm_classes import get_orm_classes
from ..common.json_responses import messages, debugmessages, infomessages
from ..common.log_method import application_logger
from ..common.info_log_method import process_logger


# Method to insert "Operator" role.
async def insert_operator(db):
    archive_viewer_log = application_logger()
    try:
        archive_viewer_log_info = process_logger()
        ormclass_dict = get_orm_classes()

        Rolemaster = ormclass_dict["Rolemaster"]

        operator_role = (
            db.query(Rolemaster.id)
            .filter(Rolemaster.rolename == messages["messagecode"]["156"])
            .first()
        )
        if operator_role is None:
            operator_permission = """{
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
                                "write": false,
                                "update": false,
                                "delete": false
                            },
                        "manageUsers":
                            {
                                "read": false,
                                "write": false,
                                "update": false,
                                "delete": false
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
                                "read": false,
                                "write": false,
                                "update": false,
                                "delete": false
                            }
                    }"""
            role_info2 = Rolemaster(
                rolename=messages["messagecode"]["156"], permission=operator_permission
            )
            db.add(role_info2)
            db.commit()
            db.refresh(role_info2)
            archive_viewer_log_info.info(infomessages["info_messages"]["5006"])

        else:
            archive_viewer_log.error(debugmessages["debug_messages"]["3237"])

    except Exception as e:
        archive_viewer_log.exception(e, exc_info=True)
        archive_viewer_log.error(debugmessages["debug_messages"]["1986"])
