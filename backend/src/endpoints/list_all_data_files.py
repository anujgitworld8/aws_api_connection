from fastapi import APIRouter
from backend.src.common.connection_load import load_credentials
from botocore.exceptions import NoCredentialsError, PartialCredentialsError, ClientError
import boto3

router = APIRouter()


@router.get("/list-files/")
async def list_files():
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

        # List objects in the S3 bucket
        response = s3_client.list_objects_v2(Bucket=credentials['s3_bucket_name'])

        # Check if the bucket is empty
        if 'Contents' not in response:
            return {"message": "No files found in the S3 bucket."}

        # Extract file names from the response
        file_list = [obj['Key'] for obj in response['Contents']]
        return {"files": file_list}

    except (NoCredentialsError, PartialCredentialsError) as e:
        return {"error": "Credentials not available"}
    except ClientError as e:
        return {"error": str(e)}
    except Exception as e:
        return {"error": str(e)}