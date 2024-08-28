from fastapi import APIRouter, UploadFile, File
from backend.src.common.connection_load import load_credentials
from botocore.exceptions import NoCredentialsError, PartialCredentialsError, EndpointConnectionError

import boto3

router = APIRouter()

@router.post("/uploadData/")
async def upload_data(file: UploadFile = File(...)):
    try:
        # Load credentials from the JSON file
        credentials = load_credentials()

        # Connect to AWS S3 
        s3_client = boto3.client(
            's3',
            aws_access_key_id=credentials['aws_access_key_id'],
            aws_secret_access_key=credentials['aws_secret_access_key'],
            region_name=credentials['aws_region_name']
        )

        # Upload image to S3 bucket
        s3_client.upload_fileobj(
            file.file, 
            credentials['s3_bucket_name'], 
            file.filename
        ) 

        # Generate URL of the uploaded image
        image_url = f"https://{credentials['s3_bucket_name']}.s3.{credentials['aws_region_name']}.amazonaws.com/{file.filename}"
        return {"url": image_url}
    except (NoCredentialsError, PartialCredentialsError) as e:
        return {"error": "Credentials not available or incomplete."}
    except EndpointConnectionError:
        return {"error": "No internet connection. Please check your network and try again."}