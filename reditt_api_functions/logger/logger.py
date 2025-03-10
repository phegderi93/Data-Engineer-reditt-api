import logging
import os
import boto3
from configs.credentials import s3_credentials
import shutil

log_dir = 'logs'
log_file = os.path.join(log_dir, "app.log")

def configure_logger():
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )

    return logging.getLogger(__name__)

logger = configure_logger()

def upload_log_to_s3():
    s3_client = boto3.client(
        's3',
        aws_access_key_id=s3_credentials['aws_access_key_id'],
        aws_secret_access_key=s3_credentials['aws_secret_access_key']
    )
    s3_bucket = "prasad-reditt-test-log"
    s3_prefix = "log_folder"
    s3_key = f"{s3_prefix}/{os.path.basename(log_file)}"

    try:
        s3_client.upload_file(log_file, s3_bucket, s3_key)
        logger.info(f"Log file uploaded to S3 at s3://{s3_bucket}/{s3_key}")
        # Remove the log directory only if the upload is successful
        if os.path.exists(log_dir):
            shutil.rmtree(log_dir)
    except boto3.exceptions.S3UploadFailedError as e:
        logger.error(f"Failed to upload log file to S3: {e}")
