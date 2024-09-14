from ..common.get_orm_classes import get_orm_classes
from ..common.log_method import application_logger
from ..common.json_responses import debugmessages, messages, infomessages
from ..common.info_log_method import process_logger


# Method to insert "Business Analyst" role.
async def insert_anyalst(db):
    archive_viewer_log = application_logger()
    try:
        archive_viewer_log_info = process_logger()
        ormclass_dict = get_orm_classes()

        Rolemaster = ormclass_dict["Rolemaster"]

        analyst_role = (
            db.query(Rolemaster.id)
            .filter(Rolemaster.rolename == messages["messagecode"]["157"])
            .first()
        )
        if analyst_role is None:
            analyst_permission = """{   
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
                                "read": true
                            },
                        "manageConnections":
                            {
                                "read": false,
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
                                "read": false,
                                "write": false,
                                "update": false,
                                "delete": false
                            },
                        "applicationSettings":
                            {
                                "read": false,
                                "write": false,
                                "update": false,
                                "delete": false
                            }
                        
                    }"""

            role_info1 = Rolemaster(
                rolename=messages["messagecode"]["157"], permission=analyst_permission
            )
            db.add(role_info1)
            db.commit()
            db.refresh(role_info1)
            archive_viewer_log_info.info(infomessages["info_messages"]["5006"])
        else:
            archive_viewer_log.error(debugmessages["debug_messages"]["3237"])

    except Exception as e:
        archive_viewer_log.exception(e, exc_info=True)
        archive_viewer_log.error(debugmessages["debug_messages"]["1984"])
