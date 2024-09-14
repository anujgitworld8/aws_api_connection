import json
from pathlib import Path
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Define the relative path to connect.json
file_path = Path('AWSConnection') / 'connect.json'

# Adjust CONFIG_PATH to find the file within the project structure
CONFIG_PATH = Path(__file__).resolve().parent.parent.parent / file_path

def load_config():
    try:
        with open(CONFIG_PATH, 'r') as f:
            config = json.load(f)
            return config
    except FileNotFoundError:
        raise Exception(f"Configuration file not found at {CONFIG_PATH}.")
    except json.JSONDecodeError:
        raise Exception("Error decoding the configuration file.")
    except Exception as e:
        raise Exception(f"An error occurred: {str(e)}")

def save_config(config):
    try:
        with open(CONFIG_PATH, 'w') as f:
            json.dump(config, f, indent=4)
    except Exception as e:
        raise Exception(f"An error occurred while saving the configuration: {str(e)}")

def get_db_url():
    config = load_config()
    rds_config = config['rds']
    return f"mysql+pymysql://{rds_config['username']}:{rds_config['password']}@{rds_config['host']}:{rds_config['port']}/{rds_config['database']}"

SQLALCHEMY_DATABASE_URL = get_db_url()

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_s3_config():
    config = load_config()
    return config['s3_connect']

