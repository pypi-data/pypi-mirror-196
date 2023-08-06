import glob
import os


from botocore.exceptions import ClientError
import boto3
from loguru import logger


def upload_to_r2(title, bucket='podcast'):
    s3 = boto3.resource(
        's3',
        endpoint_url = os.getenv('R2_ENDPOINT_URL'),
        aws_access_key_id = os.getenv('R2_ACCESS_KEY_ID'),
        aws_secret_access_key = os.getenv('R2_SECRET_ACCESS_KEY'),
    )

    filetypes = ("*.rss", "*.mp3") # the tuple of file types
    upload_files = []
    for files in filetypes:
        upload_files.extend(glob.glob(files))
    
    bucket = s3.Bucket(bucket)
    for file in upload_files:
        try:
            bucket.upload_file(file, f'{title}/{file}')
        except ClientError as e:
            logger.error(e)
