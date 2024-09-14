from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from multiprocessing.dummy import Pool as ThreadPool
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

from ..common.json_responses import errormessages, messages
from ..onboarding.errormessage import error_message
from ..common.get_parent_filepath import read_files_from_parent_dir
from ..common.open_json_file import with_open_read_json_file
from ..common.exceptions import exceptions

from .mysql_create_engine import mysql_create_engine


Base = declarative_base()


def f1(_):
    _ = Session()


def thread_worker(number):
    f1(number)


def work_parallel(numbers, thread_number=4):
    pool = ThreadPool(thread_number)
    results = pool.map(thread_worker, numbers)
    pool.close()
    pool.join()
    return results


# Dependency
def get_db():
    """Method to initialize engine"""

    generate_engine()
    db = Session()
    try:
        yield db
    finally:
        db.close()
        engine.dispose()

    Session.remove()


async def get_engine():
    """Method to create engine to create a tables"""

    generate_engine()

    try:
        db = Session()
    finally:
        db.close()
        engine.dispose()
        Session.remove()
    return db


def generate_engine():
    """Method to generate engine"""

    global engine, Session

    file_name = read_files_from_parent_dir(3)

    properties = with_open_read_json_file(file_name)

    database_type = properties["metadata_config"]["databaseType"].lower()


    if database_type == messages["messagecode"]["187"]:
        engine = mysql_create_engine(properties)

   

    else:
        exceptions(404, "404-Y", errormessages["errormessagecode"]["800"])

    try:
        engine.connect()
    except SQLAlchemyError as err:
        error = str(err.__dict__["orig"])
        error_msg, code = error_message(error)
        raise HTTPException(
            status_code=504,
            detail={
                "message": errormessages["errormessagecode"]["763"] + error_msg,
                "statusCode": 504,
                "errorCode": code,
            },
        )

    session_factory = sessionmaker(bind=engine)

    Session = scoped_session(session_factory)

    numbers = [1, 2, 3]
    work_parallel(numbers, 8)
