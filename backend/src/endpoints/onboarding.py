from fastapi import APIRouter, Depends, Response, Query, Security, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from ..connections.connect_db import get_db, get_engine
from ..connections.connect_db import get_db, get_engine
from ..common.json_responses import messages, permissions, errormessages
from ..common.exceptions import exceptions, check_duplicate_fields
from ..common.getproperties_filedata import properties_file_details
from ..login_methods.authentication import Auth
from ..login_methods.check_data import data_status
from ..roles.check_permission import check_permission
from ..base_models.onboard_model import (
    CreateUserInfo,
    CreateSuperSetUrl,
    UpdateSuperSetUrl,
    MetadataTable,
)
from ..onboarding.update_metadata import create_table, test_connection
from ..onboarding.get_metadatainfo import getjson_metadata
from ..onboarding.apps_preferences import is_application_active
from ..onboarding.superuser_status import userstatus
from ..onboarding.create_basicuser import onboard_createuser
from ..onboarding.superset_info.store_superset import store_url
from ..onboarding.superset_info.get_superset import fetch_superset_url
from ..onboarding.superset_info.update_superset_url import update_superset_url
from ..onboarding.fetch_onboard_details import get_onboard_details
from ..onboarding.delete_details import delete_onboard_deatils


from .response_headers import add_headers

# APIRouter creates path operations for user module
router = APIRouter(prefix="/v1")

security = HTTPBearer()
auth_handler = Auth()


@router.get("/health-check", tags=["Health Check"])
def health_check(response: Response):
    """API to check web server is up or down."""

    add_headers(response)
    return {"detail": {"message": "Server is up", "statusCode": 200, "errorCode": None}}


# API to decode token.
@router.get("/status", tags=["Internal APIs"], include_in_schema=False)
async def decode_token(
    response: Response, credentials: HTTPAuthorizationCredentials = Security(security)
):
    """API to decode token."""
    token = credentials.credentials
    data_status(token)
    add_headers(response)
    user_id = auth_handler.decode_token(token)
    if user_id:
        return {
            "detail": {
                "message": messages["returnmessagecode"]["601"],
                "statusCode": 200,
                "errorCode": None,
            }
        }


# API to know the metadata information present or not.
@router.get("/metadata-status", tags=["Onboarding"])
async def get_metadata_status(response: Response):
    """API to check metadata tables are created or not.\n+ True - If Metadata db test connection and table creation is done.\n+ False - If Metadata db test connection and table creation is not done."""
    add_headers(response)
    success_message = await properties_file_details()
    return {
        "detail": {"message": success_message, "statusCode": 200, "errorCode": None}
    }


# API to fetch metadata table information from JSON file
@router.get("/metadata-info", tags=["Onboarding"])
async def get_metdadatainfo(response: Response):
    """API to fetch the metadata db information."""
    add_headers(response)
    response_list = await getjson_metadata()
    if response_list:
        return {
            "detail": {
                "message": messages["returnmessagecode"]["633"],
                "data": response_list,
                "statusCode": 200,
                "errorCode": None,
            }
        }
    else:
        return {
            "detail": {
                "message": messages["returnmessagecode"]["633"],
                "data": None,
                "statusCode": 200,
                "errorCode": None,
            }
        }


# API to get Super User status.
@router.get("/superuser-status", tags=["Onboarding"])
async def superuser_status(response: Response, db: Session = Depends(get_db)):
    """API to check if super user exists or not.\n 
        - True - Super User is created.\n
        - False - Super User is not created.
    """
    add_headers(response)
    status = await userstatus(db)
    return {
        "detail": {
            "message": messages["returnmessagecode"]["634"],
            "status": status,
            "statusCode": 200,
            "errorCode": None,
        }
    }


# API to know the app prefrence.
@router.get("/app-preferences", tags=["Onboarding"])
async def app_preferences(response: Response, db: Session = Depends(get_db)):
    """API to check if all the information are filled or not while onboarding.\n
            - True - All the configuration details are filled while onboarding.
            - False - Some configuration details are not filled while onboarding.
    """
    add_headers(response)
    app_preferences = await is_application_active(db)
    if app_preferences:
        return {
            "detail": {
                "message": "Application Preferences",
                "statusCode": 200,
                "data": app_preferences,
            }
        }


# API to fetch the src.onboarding details
@router.get("/onboarding", tags=["Onboarding"])
async def getonboarding_details(
    response: Response,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Security(security),
):
    """API to get the overview of configurations filled while onboarding."""
    add_headers(response)
    token = credentials.credentials
    data_status(token)
    user_id = auth_handler.decode_token(token)
    if user_id:
        ispermission = check_permission(
            user_id,
            permissions["allfeatures"]["307"],
            permissions["apitype"]["401"],
            db,
        )
        if ispermission == True:
            response_list = await get_onboard_details(db, user_id)
            return {
                "detail": {
                    "message": messages["returnmessagecode"]["638"],
                    "data": response_list,
                    "statusCode": 200,
                    "errorCode": None,
                }
            }


@router.post("/meta-data", tags=["Onboarding"])
async def add_metadata(
    response: Response,
    request: Request,
    info: MetadataTable,
    action: str = Query(
        enum=[messages["messagecode"]["327"], messages["messagecode"]["328"]]
    ),
    
    status: str = Query(
        None,
        enum=[
            messages["messagecode"]["109"],
            messages["messagecode"]["182"],
            messages["messagecode"]["183"],
        ],
        description="""status parameter to be set only when action is set to createTables, this parameter takes one of the Arguments new, skip or drop:\n+ new:To create the new tables\n+ drop:To drop the existing table and recreate the tables\n+  skip:To continue the Process with existing table """,
    ),
):
    """API to test the Database connection and to create the tables.
        \n
    Request Body:

        - databaseType : Database type should be one of postgresql, oracle, mssql, mysql, db2.
        - host : Host/IP address of the database server. Example: hostname.domain.
        - port : Port number of the database server. Example: xxxx.
        - username : Database username.
        - psswrd : Database password.
        - databaseName : Name of the database.
    """
    add_headers(response)
    raw_data = await request.body()
    check_duplicate_fields(raw_data)

    if action == messages["messagecode"]["327"]:
        success_message = await test_connection(info, False)
        return {
            "detail": {"message": success_message, "statusCode": 200, "errorCode": None}
        }
    elif action == messages["messagecode"]["328"]:
        success_message = await test_connection(info, True)
        if success_message == messages["returnmessagecode"]["630"]:
            db = await get_engine()
            return_message, statuscode = await create_table(info, db, status)
            return {
                "detail": {
                    "message": return_message,
                    "statusCode": statuscode,
                    "errorCode": None,
                }
            }
    else:
        exceptions(422, None, errormessages["errormessagecode"]["1014"])


# API to create Super User during Onboarding.
@router.post("/onboarding-authentication", tags=["Onboarding"])
async def create_onboarduser(
    response: Response,
    request: Request,
    user_details: CreateUserInfo,
    db: Session = Depends(get_db),
):
    """API to create super user during onboarding for Basic authentication.
        \n
    Request Body:

        - loginType : Login type should be BASIC.
        - fullname : Fullname of the user.
        - username : Username for login.
        - psswrd : Password for login.
        - email : Valid email address.
    """
    add_headers(response)
    raw_data = await request.body()
    check_duplicate_fields(raw_data)

    access_token = await onboard_createuser(user_details, db, response)
    return {
        "detail": {
            "data": {"access_token": access_token},
            "message": messages["returnmessagecode"]["615"],
            "statusCode": 200,
            "errorCode": None,
        }
    }


# API to store superset url to JSON file.
@router.post("/report-url", tags=["Onboarding"])
async def storesuperseturl(
    response: Response,
    request: Request,
    item: CreateSuperSetUrl,
    skip: bool = Query(enum=[False,True]),
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Security(security),
):
    """API to add Report URL: Query parameter takes two arguments.\n + True - Skip adding Report URL.\n + False - Report URL have to be added.
        \n
    Request Body:

        superseturl : Report URL.
    """
    add_headers(response)
    raw_data = await request.body()
    check_duplicate_fields(raw_data)

    token = credentials.credentials
    data_status(token)
    user_id = auth_handler.decode_token(token)
    if user_id:
        ispermission = check_permission(
            user_id,
            permissions["allfeatures"]["307"],
            permissions["apitype"]["401"],
            db,
        )
        if ispermission == True:
            return_message = await store_url(item, skip)
            return {
                "detail": {
                    "message": return_message,
                    "statusCode": 200,
                    "errorCode": None,
                }
            }


# API to delete the onboard details.
@router.delete("/delete-details", tags=["Onboarding"])
async def delete_details(
    response: Response,
    confirmDelete: bool = Query(enum=[False,True]),
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Security(security),
):
    """API to delete metadata and LDAP server information filled during onboarding."""
    add_headers(response)
    token = credentials.credentials
    data_status(token)
    user_id = auth_handler.decode_token(token)
    if user_id:
        ispermission = check_permission(
            user_id,
            permissions["allfeatures"]["307"],
            permissions["apitype"]["404"],
            db,
        )
        if ispermission:
            if confirmDelete:
                return_message = await delete_onboard_deatils()
            else:
                return_message = messages["returnmessagecode"]["650"]
            return {
                "detail": {
                    "message": return_message,
                    "statusCode": 200,
                    "errorCode": None,
                }
            }


# API to fetch superset url from JSON file.
@router.get("/report-url", tags=["Report/Visualization"])
async def getsuperseturl(
    response: Response, credentials: HTTPAuthorizationCredentials = Security(security)
):
    """API to fetch Report URL."""
    add_headers(response)
    token = credentials.credentials
    data_status(token)
    user_id = auth_handler.decode_token(token)
    if user_id:
        superset_Url = await fetch_superset_url()
        return {
            "detail": {
                "message": messages["returnmessagecode"]["636"],
                "data": {"superseturl": superset_Url},
                "statusCode": 200,
                "errorCode": None,
            }
        }


# API to update report url in JSON file.
@router.put("/report-url", tags=["Report/Visualization"])
async def update_superseturl(
    response: Response,
    request: Request,
    item: UpdateSuperSetUrl,
    credentials: HTTPAuthorizationCredentials = Security(security),
    db: Session = Depends(get_db),
):
    """API to update Report URL.
        \n
    Request Body:

        - superseturl : Report URL.
    """
    add_headers(response)
    raw_data = await request.body()
    check_duplicate_fields(raw_data)

    token = credentials.credentials
    data_status(token)
    user_id = auth_handler.decode_token(token)
    if user_id:
        ispermission = check_permission(
            user_id,
            permissions["allfeatures"]["304"],
            permissions["apitype"]["403"],
            db,
        )
        if ispermission == True:
            return_message = await update_superset_url(item)
            return {
                "detail": {
                    "message": return_message,
                    "statusCode": 200,
                    "errorCode": None,
                }
            }

