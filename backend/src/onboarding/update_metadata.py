import base64
import json
from pathlib import Path
import sqlalchemy as sa
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.exc import SQLAlchemyError, OperationalError
from fastapi import HTTPException
from ..common.create_jsonfile import (
    metadata_configuration,
    store_skip_superseturl,
    store_superseturl,
    tables_created_status,
    write_logintype,
)
from ..common.exceptions import exceptions
from ..common.info_log_method import process_logger
from ..common.json_responses import (
    errormessages,
    infomessages,
    messages,
    properties,
    debugmessages,
)
from ..onboarding.encrypt_decrypt import json_encrypt
from ..onboarding.errormessage import error_message
from ..onboarding.insert_adminrole import insert_admin
from ..onboarding.insert_analystrole import insert_anyalst
from ..onboarding.insert_operatorrole import insert_operator
from ..onboarding.insert_superuserrole import insert_superuser



# Method to test the connection based on database type.


async def test_connection(info, saveFlag):
    archive_viewer_log_info = process_logger()
    try:
        database_types = [
          
            messages["messagecode"]["187"],
          
        ]
        # connectionTypes = [
        #     messages["messagecode"]["216"],
        #     messages["messagecode"]["217"].upper(),
        # ]
        if info.databaseType.lower() not in database_types:
            raise HTTPException(
                status_code=422,
                detail={
                    "message": errormessages["errormessagecode"]["763"]
                    + errormessages["errormessagecode"]["784"],
                    "statusCode": 422,
                    "errorCode": "422-D",
                },
            )
        elif info.databaseType.lower() != messages["messagecode"]["188"] and str(
            info.port
        ).startswith("0"):
            raise HTTPException(
                status_code=422,
                detail={
                    "message": errormessages["errormessagecode"]["763"]
                    + errormessages["errormessagecode"]["783"],
                    "statusCode": 422,
                    "errorCode": "422-E",
                },
            )
        # elif (
        #     info.databaseType.lower() == messages["messagecode"]["185"]
        # ) and connectionType not in connectionTypes:
        #     exceptions(422, None, errormessages["errormessagecode"]["1015"])
        # elif (info.databaseType.lower() == messages["messagecode"]["186"]) and (
        #     LoginType != messages["messagecode"]["223"]
        # ):
        #     exceptions(422, None, errormessages["errormessagecode"]["870"])
        # else:
            
        if info.databaseType.lower() == messages["messagecode"]["187"]:
            try:
                import urllib

                if len(info.psswrd) == 0:
                    exceptions(404, None, errormessages["errormessagecode"]["971"])
                else:
                    parsed_psswrd = urllib.parse.quote_plus(info.psswrd)
                    SQLALCHEMY_DATABASE_URL = (
                        info.databaseType.lower()
                        + "+pymysql"
                        + "://"
                        + info.username.lower()
                        + ":"
                        + parsed_psswrd
                        + "@"
                        + info.host.lower()
                        + ":"
                        + str(info.port)
                        + "/"
                        + info.databaseName.lower()
                    )
                    engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_size=30, max_overflow=20, pool_recycle=3600, pool_timeout=300)
                    engine.connect()

                    if saveFlag:
                        enc_data = json_encrypt(str(parsed_psswrd))
                        enc_data = base64.b64encode(enc_data).decode("utf-8")
                        metadata_config = {
                            "databaseType": info.databaseType,
                            "host": info.host,
                            "port": info.port,
                            "username": info.username,
                            "psswrd": enc_data,
                            "databaseName": info.databaseName,
                            "connectionType": None,
                            "loginType": None,
                        }
                        await metadata_configuration(metadata_config)
                    archive_viewer_log_info.info(
                        infomessages["info_messages"]["5011"], info.databaseType
                    )
                    return messages["returnmessagecode"]["630"]
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
                        "message": errormessages["errormessagecode"]["763"]
                        + str(e),
                        "statusCode": 422,
                        "errorCode": None,
                    },
                )
            except TypeError as e:
                raise HTTPException(
                    status_code=422,
                    detail={
                        "message": errormessages["errormessagecode"]["763"]
                        + str(e),
                        "statusCode": 422,
                        "errorCode": None,
                    },
                )
            except OperationalError as e:
                raise HTTPException(
                    status_code=422,
                    detail={
                        "message": errormessages["errormessagecode"]["763"]
                        + str(e),
                        "statusCode": 422,
                        "errorCode": None,
                    },
                )
            except Exception as e:
                raise HTTPException(
                    status_code=422,
                    detail={
                        "message": errormessages["errormessagecode"]["763"]
                        + str(e),
                        "statusCode": 422,
                        "errorCode": None,
                    },
                )


    except SQLAlchemyError as err:
        error = str(err.__dict__["orig"])
        error_msg, code = error_message(error)

        raise HTTPException(
            status_code=422,
            detail={
                "message": errormessages["errormessagecode"]["763"] + error_msg,
                "statusCode": 422,
                "errorCode": code,
            },
        )


# Method to create metadata tables based on the user input.
async def create_table(info, db, status):
    try:
        status_type = [
            messages["messagecode"]["109"].lower(),
            messages["messagecode"]["182"].lower(),
            messages["messagecode"]["183"].lower(),
        ]
        if status not in status_type:
            exceptions(422, None, errormessages["errormessagecode"]["1021"])

        archive_viewer_log_info = process_logger()
        cwd = Path(__file__).parents[3]
        fileName = cwd / "properties.json"

        with open(fileName) as fp:
            properties = json.load(fp)

        properties
        try:
            if (
                properties["metadata_config"]["databaseType"].lower()
                == messages["messagecode"]["187"]
            ):
                from ..orm_classes.mysql_orm_model import Base
        except Exception as e:
            raise HTTPException(
                status_code=422,
                detail={
                    "message": errormessages["errormessagecode"]["763"] + str(e),
                    "statusCode": 422,
                    "errorCode": None,
                },
            )

        from ..connections.connect_db import engine

        insp = sa.inspect(engine)
        existing_tables = insp.get_table_names()

        list_of_tables = Base.metadata.tables.keys()

        list_of_tables = list(list_of_tables)

        is_all_table_present = all(
            element in existing_tables for element in list_of_tables
        )
        missing_tables = [
            element for element in list_of_tables if element not in existing_tables
        ]

        # creating 'NEW' metadata tables
        if existing_tables == [] and status == messages["messagecode"]["109"].lower():
            try:
                Base.metadata.create_all(engine)
                engine.connect()
            except SQLAlchemyError as err:
                error = str(err.__dict__["orig"])
                raise HTTPException(
                    status_code=422,
                    detail={
                        "message": errormessages["errormessagecode"]["763"] + error,
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

            await tables_created_status(True)
            archive_viewer_log_info.info(infomessages["info_messages"]["5012"])
            await insert_admin(db)
            await insert_anyalst(db)
            await insert_operator(db)
            # await insert_converttype(db)
            await insert_superuser(db)
            created_tables = insp.get_table_names()
            required_tables = Base.metadata.tables.keys()
            is_all_table_present = all(
                element in required_tables for element in created_tables
            )
            if is_all_table_present:
                table_count = len(required_tables)

                return str(table_count) + messages["returnmessagecode"]["631"], 200

        # 'DROP' the existing tables and re-creating metadata tables
        elif status == messages["messagecode"]["182"].lower():
            try:
                Base.metadata.drop_all(engine)
            except SQLAlchemyError as err:
                error = str(err.__dict__["orig"])
                raise HTTPException(
                    status_code=422,
                    detail={
                        "message": errormessages["errormessagecode"]["763"] + error,
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

            try:
                Base.metadata.create_all(engine)
            except SQLAlchemyError as err:
                error = str(err.__dict__["orig"])
                raise HTTPException(
                    status_code=422,
                    detail={
                        "message": errormessages["errormessagecode"]["763"] + error,
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

            engine.connect()
            await tables_created_status(True)
            archive_viewer_log_info.info(infomessages["info_messages"]["5013"])
            await insert_admin(db)
            await insert_anyalst(db)
            await insert_operator(db)
            await insert_superuser(db)
            await write_logintype("")
            await store_superseturl("")
            await store_skip_superseturl(False)
            # await delete_storage_details()
            return messages["returnmessagecode"]["642"], 200

        # 'SKIP' the creation of metadata tables and 'CONTINUE' with existing tables
        elif existing_tables and status == messages["messagecode"]["183"].lower():
            if missing_tables != []:
                metadata = Base.metadata
                for table in missing_tables:
                    await create_specific_table(metadata, table, engine)

            await tables_created_status(True)
            # await default_location(db)
            return messages["returnmessagecode"]["644"], 100

        # Raise Exception if all the Required tables are present
        elif is_all_table_present and status == messages["messagecode"]["109"].lower():
            await clear_metadata_details()
            exceptions(409, "409-A", errormessages["errormessagecode"]["803"])

        # Raise Exception if any Rquired tables are missing
        else:
            message = {
                "error_message": errormessages["errormessagecode"]["976"],
                "missing_tables": missing_tables,
            }
            await clear_metadata_details()
            exceptions(409, "409-B", message)

    except SQLAlchemyError as err:
        error = str(err.__dict__["orig"])
        error_msg, code = error_message(error)

        raise HTTPException(
            status_code=422,
            detail={
                "message": errormessages["errormessagecode"]["763"] + error_msg,
                "statusCode": 422,
                "errorCode": code,
            },
        )


async def create_specific_table(metadata, table_name, engine):
    """Method to create a Specific table based on table name"""

    table = metadata.tables.get(str(table_name))
    table.create(engine)


async def clear_metadata_details():
    """Method to clear metadata details from properties.json file"""

    metadata_config = {
        "databaseType": "",
        "host": "",
        "port": "",
        "username": "",
        "psswrd": "",
        "databaseName": "",
        "connectionType": "",
        "loginType": "",
    }
    await metadata_configuration(metadata_config)
    await tables_created_status(False)
