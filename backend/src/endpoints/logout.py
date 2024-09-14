import base64
import logging

from datetime import datetime, timezone
from pathlib import Path

from fastapi import APIRouter, Depends, Response, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from ..connections.connect_db import get_db
from ..login_methods.authentication import Auth
from ..common.get_orm_classes import get_orm_classes
from ..common.json_responses import messages, infomessages, debugmessages
from ..common.log_method import setup_logger
from ..common.log_method import application_logger, setup_logger
from ..common.info_log_method import process_logger

from .response_headers import add_headers

# APIRouter creates path operations for user module
router = APIRouter(prefix="/v1")

security = HTTPBearer()
auth_handler = Auth()


# Logout API
@router.delete("/logout", tags=["Logout API"])
async def logout(
    response: Response,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Security(security),
):
    """API to logout from the application."""
    add_headers(response)
    token = credentials.credentials
    user_id = auth_handler.decode_token(token)
    if user_id:
        archive_viewer_log = application_logger()
        try:
            archive_viewer_log_info = process_logger()
            ormclass_dict = get_orm_classes()
            Usermaster = ormclass_dict["Usermaster"]
            logout_time = datetime.now(timezone.utc)
            cwd = Path(__file__).parents[1]
            fileName = cwd / "login_methods/.store_data.txt"
            with open(fileName, "a") as f:
                bytes_encoded = token.encode()
                enc_data = base64.b64encode(bytes_encoded).decode("utf-8")
                f.write(f"{enc_data}" + " " + str(logout_time) + "\n")
                response.delete_cookie("access_token")

            cwd_logs = Path(__file__).parents[4]
            today = datetime.now()
            dt_string = today.strftime("%d_%b_%Y")
            loginInfo = "loginInfo" + "_" + dt_string + ".log"
            logfileName = cwd_logs / "ArchiveViewer_logs" / loginInfo

            user_info = (
                db.query(Usermaster.username).filter(Usermaster.id == user_id).first()
            )
            archive_viewer_log_info.info(
                infomessages["info_messages"]["5055"], user_info[0]
            )

            with open(logfileName, "a") as _:
                login_info = setup_logger(
                    "logininfo_logger" + str(user_id), logfileName, logging.INFO
                )
                login_info.info(str(user_info[0]) + " " + "logged out successfully")
                return {
                    "detail": {
                        "message": messages["returnmessagecode"]["641"],
                        "statusCode": 200,
                        "errorCode": None,
                    }
                }
        except Exception as e:
            archive_viewer_log.exception(e, exc_info=True)
            archive_viewer_log.error(debugmessages["debug_messages"]["3085"])
