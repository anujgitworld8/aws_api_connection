# from fastapi import APIRouter, HTTPException
# from ..common.AWS_credentials import AWSCredentials 
# import json
# import os

# router = APIRouter()

# # POST API to save AWS credentials in a JSON file
# @router.post("/connect/")
# async def aws_connect(credentials: AWSCredentials):
#     try:
#         # Convert the credentials to a dictionary
#         credentials_dict = credentials.dict()

#         # Define the folder path inside the 'backend' directory
#         folder_path = os.path.join('backend', 'AWSConnection')

#         # Create the folder if it doesn't exist
#         os.makedirs(folder_path, exist_ok=True)

#         # Define the full file path
#         file_path = os.path.join(folder_path, 'connect.json')

#         # Write the credentials to the JSON file inside the folder
#         with open(file_path, 'w') as f:
#             json.dump(credentials_dict, f)

#         return {"message": "AWS credentials and S3 bucket name have been saved successfully."}

#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
