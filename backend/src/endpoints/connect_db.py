# import json
# from fastapi import APIRouter, HTTPException
# from sqlalchemy import create_engine
# from sqlalchemy.exc import SQLAlchemyError
# from sqlalchemy.sql import text
# from ..connections.config import get_db_url, save_config, load_config
# from ..common.AWS_credentials import RDSConfig
# import logging
# from urllib.parse import urlparse

# # Set up logging configuration
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# router = APIRouter()

# # Global engine variable
# engine = None

# def init_db(connection_url: str):
#     global engine
#     try:
#         # Create the engine
#         engine = create_engine(connection_url, pool_size=20, max_overflow=0)
#         # Test the connection to ensure it works
#         with engine.connect() as connection:
#             logger.info("Database connection established successfully.")
#             pass  # Perform any necessary testing or initialization
#     except SQLAlchemyError as err:
#         error = str(err.__dict__.get('orig', 'Unknown error'))
#         logger.error(f"Database connection error: {error}")
#         raise HTTPException(status_code=500, detail={"message": "Database connection error", "error": error})
#     except Exception as e:
#         logger.error(f"Failed to connect: {str(e)}")
#         raise HTTPException(status_code=500, detail={"message": "Failed to connect", "error": str(e)})

# @router.on_event("startup")
# async def startup_event():
#     # No database initialization here
#     logger.info("Application startup complete. Database connection is not initialized.")

# @router.post("/connect-database", tags=["Database connection"])
# def connect_rds(details: RDSConfig):
#     try:
#         # Create a new engine using the provided connection details
#         connection_url = f"mysql+pymysql://{details.username}:{details.password}@{details.host}:{details.port}/{details.database}"
#         test_engine = create_engine(connection_url, pool_size=20, max_overflow=0)
        
#         # Attempt to connect to the database
#         test_engine.connect()

#         # Save the connection details to connect.json
#         config = load_config()
#         config['rds'] = {
#             'username': details.username,
#             'password': details.password,
#             'host': details.host,
#             'port': details.port,
#             'database': details.database
#         }
#         save_config(config)

#         # Reinitialize the global engine with the new details
#         init_db(connection_url)

#         return {"message": "Connected to RDS MySQL successfully with provided details!"}
#     except SQLAlchemyError as err:
#         error = str(err.__dict__.get('orig', 'Unknown error'))
#         logger.error(f"Database connection error: {error}")
#         raise HTTPException(status_code=500, detail={"message": "Database connection error", "error": error})
#     except Exception as e:
#         logger.error(f"Failed to connect: {str(e)}")
#         raise HTTPException(status_code=500, detail={"message": "Failed to connect", "error": str(e)})

# @router.get("/check-database-connection", tags=["Database connection"])
# def test_connection():
#     try:
#         SQLALCHEMY_DATABASE_URL = get_db_url()  # Use the stored credentials
#         if not SQLALCHEMY_DATABASE_URL:
#             raise HTTPException(status_code=500, detail={"message": "No database URL found in config."})
        
#         logger.info(f"Attempting to connect using URL: {SQLALCHEMY_DATABASE_URL}")

#         engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_size=20, max_overflow=0)
#         with engine.connect() as conn:
#             # Use text() to ensure compatibility with newer versions of SQLAlchemy
#             conn.execute(text("SELECT 1"))  # Test connection
        
#         # Extract the database name from the connection URL
#         parsed_url = urlparse(SQLALCHEMY_DATABASE_URL)
#         database_name = parsed_url.path.strip('/')  # Remove leading slash
        
#         return {"message": f"Connected to RDS MySQL database '{database_name}' successfully!"}
#     except SQLAlchemyError as err:
#         error = str(err)
#         logger.error(f"Database connection error: {error}")
#         raise HTTPException(status_code=500, detail={"message": "Database connection error", "error": error})
#     except Exception as e:
#         logger.error(f"Failed to connect: {str(e)}")
#         raise HTTPException(status_code=500, detail={"message": "Failed to connect", "error": str(e)})