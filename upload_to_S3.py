# upload to S3

import boto3
from botocore.exceptions import NoCredentialsError
import os

def upload(local_file, bucket):
    s3 = boto3.client('s3', aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
                      aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'])
    
    s3_file_name = '{}'.format(os.path.basename(local_file))
    
    try:
        s3.upload_file(local_file, bucket, s3_file_name)
        print(str(s3_file_name) + " Upload Successful")
        return True
    except FileNotFoundError:
        print("The file was not found")
        return False
    except NoCredentialsError:
        print("Credentials not available")
        return False