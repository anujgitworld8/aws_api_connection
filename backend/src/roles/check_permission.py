from ..common.json_responses import response
from ..common.exceptions import exceptions

from .get_permissions import get_permissions


# Method to check the logged-in user have the particular permission or not.
def check_permission(user_id, feature, api_type, db):
    _, permissions = get_permissions(user_id, db)
    if permissions[feature][api_type] == True:
        return True
    else:
        exceptions(404, "404-A", response["response_msg"]["403"])
