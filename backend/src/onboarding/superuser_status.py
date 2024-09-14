from ..common.get_orm_classes import get_orm_classes
from ..common.json_responses import messages, debugmessages, infomessages
from ..common.log_method import application_logger
from ..common.info_log_method import process_logger


# Method to check Super User status.
async def userstatus(db):
    archive_viewer_log = application_logger()
    try:
        ormclass_dict = get_orm_classes()
        Usermaster = ormclass_dict["Usermaster"]
        Rolemaster = ormclass_dict["Rolemaster"]
        Userrole = ormclass_dict["Userrole"]

        archive_viewer_log_info = process_logger()

        users = (
            db.query(Usermaster.id)
            .join(Userrole, Usermaster.id == Userrole.usermasterid)
            .join(Rolemaster, Userrole.rolemasterid == Rolemaster.id)
            .filter(
                Rolemaster.rolename == messages["messagecode"]["152"],
                Usermaster.active != messages["messagecode"]["113"],
            )
            .first()
        )

        if users is not None:
            status = True
        else:
            status = False

        archive_viewer_log_info.info(infomessages["info_messages"]["5001"])
        return status

    except Exception as e:
        archive_viewer_log.exception(e, exc_info=True)
        archive_viewer_log.error(debugmessages["debug_messages"]["1987"])
