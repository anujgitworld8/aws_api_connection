import re
from typing import List, Optional
from pydantic import field_validator, BaseModel, Field
from ..common.json_responses import errormessages

# Define regex pattern constants
NAME_REGEX = r"^[A-Za-z-._]+(?: ?[A-Za-z-._]+)*$"
USERNAME_REGEX = r"^\w+$"
EMAIL_REGEX = r"^([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,3})+$"
NEW_PASSWORD_REGEX = r"^(?=.*\d)(?=.*[a-zA-Z])(?=.*[A-Z])(?=.*[a-z])(?=.*[-~#$.%&*!@^])(?!.*\s).{8,20}$"
USER_STATUS_REGEX = r"^[A-Za-z0-9_-]+$"

class AuthModel(BaseModel, extra='forbid'):
    username: str = Field(examples=["username"])
    psswrd: str = Field(examples=["psswrd"])

class SearchRequest(BaseModel, extra='forbid'):
    searchBy: str = Field(examples=["searchBy"])
    psswrd: str = Field(examples=["psswrd"])
    
class GetUserDetails(BaseModel, extra='forbid'):
    id: int = Field(examples=["id"])
    username: str = Field(examples=["username"])
    psswrd: str = Field(examples=["psswrd"])
    useremail: str = Field(examples=["useremail"])
    active: str = Field(examples=["active"])
    created_date: str = Field(examples=["createdate"])
    created_by: int = Field(examples=["created_by"])
    last_updated: str = Field(examples=["last_updated"])
    last_updated_by: int = Field(examples=["last_updated_by"])
    last_login: str = Field(examples=["last_login"])

class CreateUserDetails(BaseModel, extra='forbid'):
    name: str = Field(examples=["name"], min_length=1, max_length=1000)
    username: str = Field(examples=["username"], min_length=4, max_length=100)
    email: str = Field(examples=["email"], min_length=6, max_length=320)
    roleId: int = Field(examples=["roleId"], gt=0)

    @field_validator("name")
    @classmethod
    def validate_name(cls, value):
        if not value or not value.strip() or not re.match(NAME_REGEX, value):
            raise ValueError(errormessages["errormessagecode"]["979"] + "name")
        return value

    @field_validator("username")
    @classmethod
    def validate_username(cls, value):
        if not value or not value.strip() or not re.match(USERNAME_REGEX, value):
            raise ValueError(errormessages["errormessagecode"]["979"] + "username")
        return value

    @field_validator("email")
    @classmethod
    def validate_email(cls, value):
        if not value or not value.strip() or not re.match(EMAIL_REGEX, value):
            raise ValueError(errormessages["errormessagecode"]["979"] + "email")
        return value

class UpdateUserDetails(BaseModel, extra='forbid'):
    name: str = Field(examples=["name"], min_length=1, max_length=1000)
    email: Optional[str] = Field(None, examples=["email"])
    roleId: int = Field(examples=["roleId"], gt=0)

class UpdatePswrd(BaseModel, extra='forbid'):
    username: str = Field(examples=["username"], min_length=4, max_length=100)
    oldpsswrd: str = Field(examples=["psswrd"],min_length=8)
    newpsswrd: str = Field(examples=["psswrd"], min_length=8)

    @field_validator("username")
    @classmethod
    def validate_username(cls, value):
        if not value or not value.strip() or not re.match(USERNAME_REGEX, value):
            raise ValueError(errormessages["errormessagecode"]["979"] + "username")
        return value

    @field_validator("newpsswrd")
    @classmethod
    def validate_newpsswrd(cls, value):
        if not value or not value.strip() or not re.match(NEW_PASSWORD_REGEX, value):
            raise ValueError(errormessages["errormessagecode"]["979"] + "newpsswrd")
        return value

class UpdateStatus(BaseModel, extra='forbid'):
    username: str = Field(examples=["username"], min_length=4, max_length=100)
    userstatus: str = Field(examples=["userstatus"], min_length=6, max_length=20)

    @field_validator("username")
    @classmethod
    def validate_username(cls, value):
        if not value or not value.strip() or not re.match(USERNAME_REGEX, value):
            raise ValueError(errormessages["errormessagecode"]["979"] + "username")
        return value

    @field_validator("userstatus")
    @classmethod
    def validate_userstatus(cls, value):
        if not value or not value.strip() or not re.match(USER_STATUS_REGEX, value):
            raise ValueError(errormessages["errormessagecode"]["979"] + "userstatus")
        return value
