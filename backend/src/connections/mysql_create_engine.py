from fastapi import HTTPException
from sqlalchemy import create_engine

from ..common.json_responses import errormessages
from ..common.psswrd_decrypt import psswrd_decrypt


# Method to create engine for mysql database
def mysql_create_engine(properties):
    try:
        psswd = properties["metadata_config"]["psswrd"]
        data = psswrd_decrypt(psswd)

        SQLALCHEMY_DATABASE_URL = (
            properties["metadata_config"]["databaseType"].lower()
            + "+pymysql"
            + "://"
            + properties["metadata_config"]["username"].lower()
            + ":"
            + data
            + "@"
            + properties["metadata_config"]["host"].lower()
            + ":"
            + str(properties["metadata_config"]["port"]).lower()
            + "/"
            + properties["metadata_config"]["databaseName"].lower()
        )
        engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_size=30, max_overflow=20, pool_recycle=3600, pool_timeout=300)
        return engine

    except ImportError:
        raise HTTPException(
            status_code=422,
            detail={
                "message": errormessages["errormessagecode"]["839"],
                "statusCode": 422,
                "errorCode": "422-L",
            },
        )
    except AttributeError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "message": errormessages["errormessagecode"]["763"] + str(e),
                "statusCode": 422,
                "errorCode": None,
            },
        )
    except TypeError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "message": errormessages["errormessagecode"]["763"] + str(e),
                "statusCode": 422,
                "errorCode": None,
            },
        )
    except Exception as e:
        raise HTTPException(
            status_code=422,
            detail={
                "message": errormessages["errormessagecode"]["763"] + str(e),
                "statusCode": 422,
                "errorCode": None,
            },
        )
