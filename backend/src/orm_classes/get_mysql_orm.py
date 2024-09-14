from ..common.log_method import application_logger
from ..common.json_responses import debugmessages


def get_mysql_orm():
    archive_viewer_log = application_logger()
    try:
        from ..orm_classes import mysql_orm_model

        response_dict = dict()
        response_dict["Usermaster"] = mysql_orm_model.Usermaster
        # response_dict["Appmaster"] = mysql_orm_model.Appmaster
        # response_dict["Convertservermaster"] = mysql_orm_model.Convertservermaster
        # response_dict["Converttypemaster"] = mysql_orm_model.Converttypemaster
        # response_dict["Queryservermaster"] = mysql_orm_model.Queryservermaster
        response_dict["Rolemaster"] = mysql_orm_model.Rolemaster
        response_dict["Userrole"] = mysql_orm_model.Userrole
        # response_dict["Archivefiletracktemp"] = mysql_orm_model.Archivefiletracktemp
        # response_dict["ProcesstrackerCsv"] = mysql_orm_model.ProcesstrackerCsv
        # response_dict["Archivefiletrack"] = mysql_orm_model.Archivefiletrack
        # response_dict["UtilityMonitor"] = mysql_orm_model.UtilityMonitor
        # response_dict["Convertrequest"] = mysql_orm_model.Convertrequest
        # response_dict["ProcesstrackerParquet"] = mysql_orm_model.ProcesstrackerParquet
        # response_dict["Csvfiletrack"] = mysql_orm_model.Csvfiletrack
        # response_dict["TableMaster"] = mysql_orm_model.TableMaster
        # response_dict["Parquetfiletrack"] = mysql_orm_model.Parquetfiletrack
        # response_dict["ProcessdetailsParquet"] = mysql_orm_model.ProcessdetailsParquet
        # response_dict["ProcessdetailsCsv"] = mysql_orm_model.ProcessdetailsCsv
        # # response_dict["ProcesstrackerExternaltable"] = (
        # #     mysql_orm_model.ProcesstrackerExternaltable
        # # )
        # response_dict["ProcessdetailsExternaltable"] = (
        #     mysql_orm_model.ProcessdetailsExternaltable
        # )

        return response_dict
    except Exception as e:
        archive_viewer_log.exception(e, exc_info=True)
        archive_viewer_log.error(debugmessages["debug_messages"]["2046"])
