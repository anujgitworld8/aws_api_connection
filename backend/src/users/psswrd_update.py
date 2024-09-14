import hashlib
import base64

from datetime import datetime, timezone, timedelta

from ..common.get_orm_classes import get_orm_classes
from ..common.exceptions import exceptions
from ..login_methods.authentication import Auth
from ..common.json_responses import (
    messages,
    errormessages,
    debugmessages,
    infomessages,
)
from ..common.log_method import application_logger
from ..common.info_log_method import process_logger

from .psswrd_hash import hashpsswrd

auth_handler = Auth()


# Method to add new psswrd for specific user.
def add_newpssword(username, psswrd, db):
    ormclass_dict = get_orm_classes()
    Usermaster = ormclass_dict["Usermaster"]
    archive_viewer_log_info = process_logger()

    username = username.lower()
    hashedpsswrd, salt = hashpsswrd(psswrd)
    exp_date = datetime.now() + timedelta(days=90)
    archive_viewer_log = application_logger()
    try:
        db.query(Usermaster).filter(Usermaster.username == username).update(
            {
                Usermaster.psswrd: hashedpsswrd,
                Usermaster.salt: salt,
                Usermaster.active: messages["messagecode"]["115"],
                Usermaster.psswrd_exp_date: exp_date,
            }
        )
        db.commit()

        archive_viewer_log_info.info(infomessages["info_messages"]["5036"])

    except Exception as e:
        archive_viewer_log.exception(e, exc_info=True)
        archive_viewer_log.error(debugmessages["debug_messages"]["3026"])


# Method to update psswrd of specific user.
async def psswrd_update(item, db):
    ormclass_dict = get_orm_classes()
    Usermaster = ormclass_dict["Usermaster"]

    username = item.username.lower()

    user_info = (
        db.query(Usermaster.salt, Usermaster.psswrd)
        .filter(
            Usermaster.username == username,
            Usermaster.active != messages["messagecode"]["171"],
            Usermaster.active != messages["messagecode"]["172"],
        )
        .first()
    )

    if user_info is None:
        exceptions(404, None, errormessages["errormessagecode"]["723"])
    elif user_info.salt is None:
        user_newpsswrd = user_info.psswrd
        base64_bytes = user_newpsswrd.encode("ascii")
        message_bytes = base64.b64decode(base64_bytes)
        temp_psswrd = message_bytes.decode("ascii")

        if item.oldpsswrd != temp_psswrd:
            exceptions(404, "404-A", errormessages["errormessagecode"]["702"])
        elif temp_psswrd == item.newpsswrd:
            exceptions(409, "409-A", errormessages["errormessagecode"]["813"])
        else:
            add_newpssword(item.username.lower(), item.newpsswrd, db)
            return messages["returnmessagecode"]["616"]
    else:
        new_psswrd = item.newpsswrd.encode()
        digest = hashlib.pbkdf2_hmac("sha512", new_psswrd, user_info[0], 10000)
        hex_hash = digest.hex()
        hashedpsswrd = hex_hash

        old_psswrd = item.oldpsswrd.encode()
        digest = hashlib.pbkdf2_hmac("sha512", old_psswrd, user_info[0], 10000)
        hex_hash = digest.hex()
        old_hashedpsswrd = hex_hash

        if old_hashedpsswrd != user_info[1]:
            exceptions(404, "404-A", errormessages["errormessagecode"]["702"])
        elif user_info[1] == hashedpsswrd:
            exceptions(419, "419-A", errormessages["errormessagecode"]["813"])
        else:
            add_newpssword(item.username.lower(), item.newpsswrd, db)
            return messages["returnmessagecode"]["616"]
