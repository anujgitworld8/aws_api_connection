import re
from typing import Optional
from pydantic import field_validator, AnyUrl, BaseModel, Field
from ..common.json_responses import errormessages

# Define regex pattern constants
LOGIN_TYPE_REGEX = r"^[A-Za-z ]+$"
DNS_IP_REGEX = r"^([a-zA-Z0-9]|[a-zA-Z0-9][a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])(\.([a-zA-Z0-9]|[a-zA-Z0-9][a-zA-Z0-9\-]{0,61}[a-zA-Z0-9]))*$"
BASE_DN_REGEX = r"^[A-Za-z0-9_= ,()]+$"
FULLNAME_REGEX = r"^[A-Za-z_ ]+$"
USERNAME_REGEX = r"^\w+$"
PASSWORD_REGEX = r"^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[-~#$.%&*!@^]).{8,20}$"
EMAIL_REGEX = r"^([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,3})+$"

class CreateSuperSetUrl(BaseModel, extra='forbid'):
    superseturl: Optional[str] = Field(None, examples=['https://example.com'])


class UpdateSuperSetUrl(BaseModel, extra='forbid'):
    superseturl: AnyUrl = Field(examples=['https://example.com'])

class CreateUserInfo(BaseModel, extra='forbid'):
    loginType: str = Field(examples=["loginType"], min_length=1)
    fullname: str = Field(examples=["name"], min_length=1, max_length=1000)
    username: str = Field(examples=["username"], min_length=4, max_length=100)
    psswrd: str = Field(examples=["psswrd"], min_length=8)
    email: str = Field(examples=["email"], min_length=6, max_length=320)

    @field_validator("loginType")
    @classmethod
    def validate_loginType(cls, value):
        if not value or not value.strip() or not re.match(LOGIN_TYPE_REGEX, value):
            raise ValueError(
                errormessages["errormessagecode"]["979"] + "loginType")
        return value

    @field_validator("fullname")
    @classmethod
    def validate_fullname(cls, value):
        if not value or not value.strip() or not re.match(FULLNAME_REGEX, value):
            raise ValueError(
                errormessages["errormessagecode"]["979"] + "fullname")
        return value

    @field_validator("username")
    @classmethod
    def validate_username(cls, value):
        if not value or not value.strip() or not re.match(USERNAME_REGEX, value):
            raise ValueError(
                errormessages["errormessagecode"]["979"] + "username")
        return value

    @field_validator("psswrd")
    @classmethod
    def validate_psswrd(cls, value):
        if not value or not value.strip() or not re.match(PASSWORD_REGEX, value):
            raise ValueError(
                errormessages["errormessagecode"]["979"] + "psswrd")
        return value

    @field_validator("email")
    @classmethod
    def validate_email(cls, value):
        if not value or not value.strip() or not re.match(EMAIL_REGEX, value):
            raise ValueError(
                errormessages["errormessagecode"]["979"] + "email")
        return value


class MetadataTable(BaseModel, extra='forbid'):
    databaseType: str = Field(examples=["databaseType"], min_length=1)
    host: str = Field(examples=["host"], min_length=2)
    port: int = Field(examples=["port"], ge=0, le=65535)
    username: str = Field(examples=["username"], min_length=1)
    psswrd: str = Field(examples=["psswrd"], min_length=1)
    databaseName: str = Field(examples=["databaseName"], min_length=1)
