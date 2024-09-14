from src.common.get_orm_classes import get_orm_classes
from src.common.json_responses import debugmessages, infomessages
from src.common.log_method import application_logger
from src.common.info_log_method import process_logger


# Method to delete the role(s) for specific user.
async def delete_userroles(usermasterid, rolemasterid, db):
    archive_viewer_log = application_logger()
    try:
        archive_viewer_log_info = process_logger()
        ormclass_dict = get_orm_classes()
        Userrole = ormclass_dict["Userrole"]

        userrole_info = (
            db.query(Userrole)
            .filter(
                Userrole.usermasterid == usermasterid,
                Userrole.rolemasterid == rolemasterid,
            )
            .first()
        )
        db.delete(userrole_info)
        db.commit()

        archive_viewer_log_info.info(infomessages["info_messages"]["5031"])

    except Exception as e:
        archive_viewer_log.exception(e, exc_info=True)
        archive_viewer_log.error(debugmessages["debug_messages"]["1963"])
