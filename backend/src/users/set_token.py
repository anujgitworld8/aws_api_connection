from ..common.get_orm_classes import get_orm_classes
from ..login_methods.authentication import Auth
from ..common.exceptions import exceptions
from ..common.json_responses import errormessages


auth_handler = Auth()


# Method to fetch the user token using username.
def user_auth(username, db):
    ormclass_dict = get_orm_classes()
    Usermaster = ormclass_dict["Usermaster"]

    user_id = db.query(Usermaster.id).filter(Usermaster.username == username).first()

    if user_id is None:
        exceptions(404, None, errormessages["errormessagecode"]["723"])
    else:
        id_user = user_id.id
        access_token = auth_handler.encode_token(str(id_user))
        return access_token
