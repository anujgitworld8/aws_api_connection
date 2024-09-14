from fastapi import APIRouter, Depends, Response, Request
from sqlalchemy.orm import Session

from ..common.exceptions import check_duplicate_fields

from ..base_models.user_model import AuthModel
from ..login_methods.login import user_login
from ..connections.connect_db import get_db
from ..common.json_responses import messages

from .response_headers import add_headers

router = APIRouter(prefix="/v1")


# Login API.
@router.post("/login", tags=["Login API"])
async def login(
    response: Response,
    request: Request,
    user_details: AuthModel,
    db: Session = Depends(get_db),
):
    """API to login to the application.
        \n
    Request Body:

        Username : Valid Username.
        Psswrd : User Password.
    """
    add_headers(response)
    raw_data = await request.body()
    check_duplicate_fields(raw_data)

    access_token, last_login = await user_login(response, user_details, db)
    return {
        "detail": {
            "data": {"access_token": access_token, "lastLogin": last_login},
            "message": messages["returnmessagecode"]["601"],
            "statusCode": 200,
            "errorCode": None,
        }
    }
