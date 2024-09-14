from ..common.json_responses import messages, errormessages


# Method to findout the particular error.
def error_message(error):
    if (
        errormessages["errormessagecode"]["830"] in error
        or errormessages["errormessagecode"]["845"] in error
        or errormessages["errormessagecode"]["846"] in error
        or errormessages["errormessagecode"]["853"] in error
    ):
        return error, "422-A"
    elif (
        messages["messagecode"]["162"] in error
        or errormessages["errormessagecode"]["847"] in error
        or errormessages["errormessagecode"]["852"] in error
    ):
        return error, "422-B"
    elif (
        errormessages["errormessagecode"]["831"] in error
        or errormessages["errormessagecode"]["848"] in error
    ):
        return error, "422-E"
    elif errormessages["errormessagecode"]["832"] in error:
        return errormessages["errormessagecode"]["833"], "422-F"
    elif (
        errormessages["errormessagecode"]["840"] in error
        or errormessages["errormessagecode"]["841"] in error
        or errormessages["errormessagecode"]["842"] in error
        or errormessages["errormessagecode"]["843"] in error
    ):
        return errormessages["errormessagecode"]["844"], "422-M"
    else:
        return error, "422-C"
