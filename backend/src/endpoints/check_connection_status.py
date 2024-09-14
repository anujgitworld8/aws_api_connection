# from fastapi import APIRouter
# from ..common.connection_load import load_credentials
# import boto3
# from botocore.exceptions import NoCredentialsError, PartialCredentialsError, ClientError, EndpointConnectionError


# router = APIRouter()


# @router.get("/getConnectionStatus/")
# async def get_connection_status():
#     try:
#         # Load credentials from the JSON file
#         credentials = load_credentials()

#         # Connect to AWS S3
#         s3_client = boto3.client(
#             's3',
#             aws_access_key_id=credentials['aws_access_key_id'],
#             aws_secret_access_key=credentials['aws_secret_access_key'],
#             region_name=credentials['aws_region_name']
#         )

#         # Attempt to list objects in the S3 bucket to confirm connection
#         s3_client.list_objects_v2(Bucket=credentials['s3_bucket_name'])

#         return {"message": "Successfully connected to the AWS S3 bucket."}

#     except (NoCredentialsError, PartialCredentialsError) as e:
#         return {"error": "Credentials not available or incomplete."}
#     except EndpointConnectionError:
#         return {"error": "No internet connection. Please check your network and try again."}
#     except ClientError as e:
#         error_code = e.response['Error']['Code']
#         if error_code == 'AccessDenied':
#             return {"error": "Access to the S3 bucket is denied. Please check your permissions."}
#         elif error_code == 'NoSuchBucket':
#             return {"error": f"The specified bucket '{credentials['s3_bucket_name']}' does not exist."}
#         else:
#             return {"error": f"An error occurred: {str(e)}"}
#     except Exception as e:
#         return {"error": str(e)}