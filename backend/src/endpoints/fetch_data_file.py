from fastapi import APIRouter
from botocore.exceptions import NoCredentialsError, PartialCredentialsError, ClientError
from backend.src.common.connection_load import load_credentials
import boto3

router = APIRouter()
@router.get("/download/")
async def download_data_file(file_name: str):
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

        # Check if the file exists
        try:
            s3_client.head_object(Bucket=credentials['s3_bucket_name'], Key=file_name)
        except ClientError as e:
            if e.response['Error']['Code'] == "404":
                return {"error": f"File '{file_name}' not found in the S3 bucket."}
            else:
                return {"error": str(e)}

        # Generate a presigned URL for the file
        presigned_url = s3_client.generate_presigned_url(
            'get_object',
            Params={'Bucket': credentials['s3_bucket_name'], 'Key': file_name},
            ExpiresIn=3600  # URL expires in 1 hour
        )

        return {"url": presigned_url}

    except (NoCredentialsError, PartialCredentialsError) as e:
        return {"error": "Credentials not available"}
    except Exception as e:
        return {"error": str(e)}