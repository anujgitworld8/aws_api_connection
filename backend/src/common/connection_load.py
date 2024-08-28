import os
import json
from fastapi import HTTPException

# Function to load credentials from the JSON file
def load_credentials():
    try:
        # Correctly define the file path
        file_path = os.path.join('backend', 'AWSConnection', 'connect.json')

        # Open and load the JSON file
        with open(file_path, 'r') as f:
            return json.load(f)
    
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Credentials file not found.")
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Error decoding JSON file.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
