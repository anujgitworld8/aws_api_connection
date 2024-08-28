from fastapi import APIRouter
from backend.src.common.connection_load import load_credentials
from botocore.exceptions import NoCredentialsError, PartialCredentialsError, EndpointConnectionError, ClientError
from typing import Optional
import boto3
from datetime import datetime
import json

router = APIRouter()


@router.get("/view-sensor-records/")
async def view_sensor_data(file_name: str, id: Optional[str] = None, dataCreateDate_gt: Optional[str] = None, dataCreateDate_lt: Optional[str] = None):
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

        # Retrieve the JSON file from S3
        s3_object = s3_client.get_object(Bucket=credentials['s3_bucket_name'], Key=file_name)
        
        # Read the content of the JSON file
        json_data = s3_object['Body'].read().decode('utf-8')
        
        # Parse the JSON content
        parsed_data = json.loads(json_data)

        # Initialize filtered data with all records
        filtered_data = parsed_data['sensors']

        # Filter by sensor_id if provided
        if id:
            filtered_data = [sensor for sensor in filtered_data if sensor.get('sensor_id') == id]

        # Convert the date strings to datetime objects if provided
        if dataCreateDate_gt:
            dataCreateDate_gt_dt = datetime.strptime(dataCreateDate_gt, "%Y-%m-%dT%H:%M:%SZ")
            filtered_data = [sensor for sensor in filtered_data if datetime.strptime(sensor['timestamp'], "%Y-%m-%dT%H:%M:%SZ") > dataCreateDate_gt_dt]
        
        if dataCreateDate_lt:
            dataCreateDate_lt_dt = datetime.strptime(dataCreateDate_lt, "%Y-%m-%dT%H:%M:%SZ")
            filtered_data = [sensor for sensor in filtered_data if datetime.strptime(sensor['timestamp'], "%Y-%m-%dT%H:%M:%SZ") < dataCreateDate_lt_dt]

        # Return the filtered data or a message if no data is found
        if filtered_data:
            return {"data": filtered_data}
        else:
            return {"message": "No sensor data found matching the criteria."}

    except (NoCredentialsError, PartialCredentialsError) as e:
        return {"error": "Credentials not available or incomplete."}
    except EndpointConnectionError:
        return {"error": "No internet connection. Please check your network and try again."}
    except ClientError as e:
        error_code = e.response['Error']['Code']
        if error_code == "NoSuchKey":
            return {"error": f"File '{file_name}' not found in the S3 bucket."}
        elif error_code == 'AccessDenied':
            return {"error": "Access to the S3 bucket is denied. Please check your permissions."}
        else:
            return {"error": f"An error occurred: {str(e)}"}
    except json.JSONDecodeError:
        return {"error": "Error decoding the JSON file."}
    except Exception as e:
        return {"error": str(e)}