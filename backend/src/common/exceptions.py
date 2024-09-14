import json
from fastapi import HTTPException
from ..common.json_responses import errormessages


# Method to raise the exception based on statuscode, errorcode and errormessage
def exceptions(statuscode, errorcode, message):
    raise HTTPException(
        status_code=statuscode,
        detail={"message": message, "statusCode": statuscode, "errorCode": errorcode},
    )


def check_duplicate_fields(request):
    """Method to validate a Duplicate elements in a Request Body"""
    try:
        # Loads data in List of tuple eg:  [(key,value),(key,value)] and validate for Duplicate keys
        data = json.loads(
            request,
            object_pairs_hook=lambda pairs: [(key, value) for key, value in pairs],
        )
        seen_fields = set()
        for key, value in data:
            if key in seen_fields:
                raise HTTPException(
                    status_code=400,
                    detail={
                        "message": errormessages["errormessagecode"]["1012"] + str(key),
                        "statusCode": 400,
                        "errorCode": None,
                    },
                )
            seen_fields.add(key)
    except json.JSONDecodeError as e:
        raise HTTPException(
            status_code=400,
            detail={
                "message": errormessages["errormessagecode"]["1013"] + str(e),
                "statusCode": 400,
                "errorCode": None,
            },
        )
