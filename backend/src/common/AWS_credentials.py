from pydantic import BaseModel

# Define a Pydantic model for the credentials
class AWSCredentials(BaseModel):
    aws_access_key_id: str
    aws_secret_access_key: str
    aws_region_name: str
    s3_bucket_name: str 