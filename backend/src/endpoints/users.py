from fastapi import APIRouter, Depends, Response, Query, Security, Request, Header
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from typing import Union

from ..base_models.user_model import (
    CreateUserDetails,
    UpdateUserDetails,
    UpdatePswrd,
    UpdateStatus,
    SearchRequest
)
# from src.base_models.onboard_model import CreateLDAPUser
from ..connections.connect_db import get_db
from ..common.json_responses import messages, permissions, errormessages
from ..common.exceptions import exceptions, check_duplicate_fields
from ..common.get_orm_classes import get_orm_classes
from ..login_methods.authentication import Auth
from ..login_methods.check_data import data_status
from ..roles.check_permission import check_permission
from ..users.create_user import user_create
from ..users.get_user import get_all_users
from ..users.update_user import user_update
from ..users.delete_user import user_delete
from ..users.change_status import modify_status_new
from ..users.set_token import user_auth
from ..users.psswrd_update import psswrd_update
# from src.ldap.import_user import import_user
# from src.ldap.search_user import search_ldap_users


from .response_headers import add_headers

# APIRouter creates path operations for user module
router = APIRouter(prefix="/v1")

security = HTTPBearer()
auth_handler = Auth()


# API to get logged in user information.
@router.get("/loggedin-userinfo", tags=["Login API"])
async def get_user_info(
    response: Response,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Security(security),
):
    """API to fetch the information of logged in user."""
    add_headers(response)
    token = credentials.credentials
    data_status(token)
    user_id = auth_handler.decode_token(token)
    if user_id:
        name_list = []
        ormclass_dict = get_orm_classes()
        Usermaster = ormclass_dict["Usermaster"]

        user_info = (
            db.query(
                Usermaster.id,
                Usermaster.username,
                Usermaster.useremail,
                Usermaster.created_date,
                Usermaster.last_updated,
                Usermaster.last_login,
                Usermaster.active,
                Usermaster.fullname,
            )
            .filter(Usermaster.id == user_id)
            .first()
        )
        name_list = {
            "id": user_info.id,
            "userName": user_info.username,
            "userEmail": user_info.useremail,
            "created_date": user_info.created_date,
            "last_updated": user_info.last_updated,
            "last_login": user_info.last_login,
            "active": user_info.active,
            "fullName": user_info.fullname,
        }

        return {
            "detail": {
                "message": messages["returnmessagecode"]["602"],
                "data": name_list,
                "statusCode": 200,
                "errorCode": None,
            }
        }


# API to check if a user is new user or not.
@router.get("/validate-username", tags=["Internal APIs"], include_in_schema=False)
async def get_username(
    response: Response,
    username: str = Query(description="""Query parameter accepts username"""),
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Security(security),
):
    """API to check if username already exists or not."""
    add_headers(response)
    token = credentials.credentials
    data_status(token)
    user_id = auth_handler.decode_token(token)
    if user_id:
        ormclass_dict = get_orm_classes()
        Usermaster = ormclass_dict["Usermaster"]
        ispermission = check_permission(
            user_id,
            permissions["allfeatures"]["305"],
            permissions["apitype"]["401"],
            db,
        )
        if ispermission == True:
            if len(username) == 0:
                exceptions(422, None, errormessages["errormessagecode"]["762"])
            else:
                username = (
                    db.query(Usermaster.username)
                    .filter(Usermaster.username == username)
                    .first()
                )
                if username is None:
                    return {
                        "detail": {
                            "message": messages["returnmessagecode"]["623"],
                            "statusCode": 200,
                            "errorCode": None,
                        }
                    }
                else:
                    exceptions(409, None, errormessages["errormessagecode"]["725"])


# API to get all the user information.
@router.get("/users", tags=["User Management"])
async def get_users(
    response: Response,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Security(security),
):
    """API to fetch all the users."""
    token = credentials.credentials
    add_headers(response)
    data_status(token)
    user_id = auth_handler.decode_token(token)
    if user_id:
        ispermission = check_permission(
            user_id,
            permissions["allfeatures"]["305"],
            permissions["apitype"]["401"],
            db,
        )
        if ispermission == True:
            response_list = await get_all_users(user_id, db)
            return {
                "detail": {
                    "data": response_list,
                    "message": messages["returnmessagecode"]["614"],
                    "statusCode": 200,
                    "errorCode": None,
                }
            }


# API to create new user.
@router.post("/user", tags=["User Management"])
async def create_user(
    response: Response,
    request: Request,
    item: CreateUserDetails,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Security(security),
):
    """API to create new BASIC user.
        \n
    Request Body:

        - name : Fullname of the user.
        - username : A unique name to identify the user within the application.
        - email : Valid email address.
        - roleId : Assign a role to the user by providing the corresponding role ID, To get the roleid use /roles API.
    """
    token = credentials.credentials
    add_headers(response)
    raw_data = await request.body()
    check_duplicate_fields(raw_data)

    data_status(token)
    user_id = auth_handler.decode_token(token)
    if user_id:
        ispermission = check_permission(
            user_id,
            permissions["allfeatures"]["305"],
            permissions["apitype"]["402"],
            db,
        )
        if ispermission == True:
            user_data = await user_create(item, user_id, db)
            return {
                "detail": {
                    "message": messages["returnmessagecode"]["615"],
                    "data": [user_data],
                    "statusCode": 200,
                    "errorCode": None,
                }
            }


# API to change status of specific user.


@router.put("/alter-status", tags=["User Management"])
async def status_change(
    response: Response,
    request: Request,
    userinfo: UpdateStatus,
    db: Session = Depends(get_db),
):
    """API to change the status of specific user.
        \n
    Request Body:

        - Username : Valid username (already defined).
        - Userstatus: To update the user status (active , new-user , inactive).
    """
    add_headers(response)
    raw_data = await request.body()
    check_duplicate_fields(raw_data)

    user_name = userinfo.username.lower()
    token = user_auth(user_name, db)
    data_status(token)
    user_id = auth_handler.decode_token(token)
    if user_id:
        if (
            userinfo.userstatus == messages["messagecode"]["114"]
            or userinfo.userstatus == messages["messagecode"]["115"]
            or userinfo.userstatus == messages["messagecode"]["171"]
            or userinfo.userstatus == messages["messagecode"]["172"]
        ):
            message = await modify_status_new(userinfo, db)
            return {
                "detail": {"message": message, "statusCode": 200, "errorCode": None}
            }
        else:
            exceptions(422, None, errormessages["errormessagecode"]["923"])


# API to update user details.
@router.put("/user", tags=["User Management"])
async def update_user(
    response: Response,
    request: Request,
    info: UpdateUserDetails,
    userId: int = Query(
        description="""User id of a particlar user, To get the userId use /users API."""
    ),
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Security(security),
):
    """API to update user details based on user id.
        \n
        Note - LDAP user only can update role
    Request Body:

        - Name : Fullname of the user.
        - Email : Valid email address.  
        - Roleid : Roleid of a particular user, To get the roleid use /roles API.
    """
    token = credentials.credentials
    add_headers(response)
    raw_data = await request.body()
    check_duplicate_fields(raw_data)

    data_status(token)
    user_id = auth_handler.decode_token(token)
    if user_id:
        ispermission = check_permission(
            user_id,
            permissions["allfeatures"]["305"],
            permissions["apitype"]["403"],
            db,
        )
        if ispermission == True:
            usermasterId = userId
            message = await user_update(usermasterId, info, user_id, db)
            return {
                "detail": {"message": message, "statusCode": 200, "errorCode": None}
            }


# API to update the status of an user to 'deleted'.
@router.put("/user-deletion", tags=["User Management"])
async def delete_user(
    response: Response,
    request: Request,
    userId: int = Query(
        description="""User id of a particular user, To get the userId use /users API."""
    ),
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Security(security),
):
    """API to delete specific user based on userId."""
    token = credentials.credentials
    add_headers(response)

    data_status(token)
    user_id = auth_handler.decode_token(token)
    if user_id:
        ispermission = check_permission(
            user_id,
            permissions["allfeatures"]["305"],
            permissions["apitype"]["404"],
            db,
        )
        if ispermission == True:
            message = await user_delete(userId, user_id, db)
            return {
                "detail": {"message": message, "statusCode": 200, "errorCode": None}
            }


# API to update walkthrough of specific user.
@router.put("/psswrd-reset", tags=["User Management"])
async def update_psswrd(
    response: Response,
    request: Request,
    info: UpdatePswrd,
    db: Session = Depends(get_db),
):
    """API to update password of specific user.
        \n
    Request Body:

        - Username : Valid username (already defined).
        - Oldpsswrd : To get the temporary password for new user, use /users API.
        - Newpsswrd : New password for the user.
    """
    add_headers(response)
    raw_data = await request.body()
    check_duplicate_fields(raw_data)
    token = user_auth(info.username.lower(), db)
    user_id = auth_handler.decode_token(token)
    if user_id:
        message = await psswrd_update(info, db)
        return {"detail": {"message": message, "statusCode": 200, "errorCode": None}}


# # API to search LDAP users.
# @router.get("/ldap-user", tags=["LDAP APIs"])
# async def search_ldapuser(
#     response: Response,
#     attribute: str = Query(
#         enum=["uid", "CN", "sAMAccountName", "distinguishedName"],
#         description="""To search the LDAP user. Ex : uid, CN, sAMAccountName, distinguishedName""",
#     ),
#     searchBy: str = Query(description="""Name of the LDAP user"""),
#     psswrd: str = Header(description="""Provide logged-in user password"""),
#     db: Session = Depends(get_db),
#     credentials: HTTPAuthorizationCredentials = Security(security),
# ):
#     """API to search the Ldap-users based on attribute."""
#     add_headers(response)
#     token = credentials.credentials
#     data_status(token)
#     user_id = auth_handler.decode_token(token)
#     if user_id:
#         ispermission = check_permission(
#             user_id,
#             permissions["allfeatures"]["307"],
#             permissions["apitype"]["401"],
#             db,
#         )
#         if ispermission == True:
#             response_list = await search_ldap_users(
#                 psswrd, attribute, searchBy, db, user_id
#             )
#             return {
#                 "detail": {
#                     "message": messages["returnmessagecode"]["614"],
#                     "data": response_list,
#                     "statusCode": 200,
#                     "errorCode": None,
#                 }
#             }


# # API to import LDAP users.
# @router.post("/import-ldapuser", tags=["LDAP APIs"])
# async def import_ldapuser(
#     user_info: CreateLDAPUser,
#     request: Request,
#     response: Response,
#     db: Session = Depends(get_db),
#     credentials: HTTPAuthorizationCredentials = Security(security),
# ):
#     """API to import the LDAP user.
#         \n
#     Request Body:

#         - userName : Unique user name of the particular user.
#         - fullname : Full name of the user.
#         - roleId : Roleid of the particular user. To get the roleid use /roles API.
#         - mail: Email of the user.
#         - password: Password of the logged in user.
#     """
#     add_headers(response)
#     raw_data = await request.body()
#     check_duplicate_fields(raw_data)

#     token = credentials.credentials
#     data_status(token)
#     user_id = auth_handler.decode_token(token)
#     if user_id:
#         ispermission = check_permission(
#             user_id,
#             permissions["allfeatures"]["307"],
#             permissions["apitype"]["402"],
#             db,
#         )
#         if ispermission == True:
#             return_message = await import_user(user_info, db, user_id, user_info.password)
#             return {
#                 "detail": {
#                     "message": return_message,
#                     "statusCode": 200,
#                     "errorCode": None,
#                 }
#             }

# # API to search LDAP users.
# @router.post("/ldap-user", tags=["LDAP APIs"])
# async def search_ldapuser(
#     request: SearchRequest,
#     attribute: str = Query(
#         enum=["uid", "CN", "sAMAccountName", "distinguishedName"],
#         description="""To search the LDAP user. Ex : uid, CN, sAMAccountName, distinguishedName""",
#     ),
#     db: Session = Depends(get_db),
#     credentials: HTTPAuthorizationCredentials = Security(security),
# ):
#     """API to search the LDAP users based on attribute."""
#     token = credentials.credentials
#     data_status(token)
#     user_id = auth_handler.decode_token(token)
#     if user_id:
#         ispermission = check_permission(
#             user_id,
#             permissions["allfeatures"]["307"],
#             permissions["apitype"]["401"],
#             db,
#         )
#         if ispermission:
#             response_list = await search_ldap_users(
#                 request.psswrd, attribute, request.searchBy, db, user_id
#             )
#             return {
#                 "detail": {
#                     "message": messages["returnmessagecode"]["614"],
#                     "data": response_list,
#                     "statusCode": 200,
#                     "errorCode": None,
#                 }
#             }