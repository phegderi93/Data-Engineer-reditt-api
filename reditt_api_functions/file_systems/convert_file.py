import os
import pandas as pd
import shutil
from reditt_api_functions.logger.logger import logger
from configs.credentials import s3_credentials
from reditt_api_functions.s3_operations.s3_operations import S3Client
import pyarrow
import boto3
class ConvertFile:
    def __init__(self):
        self.tmp_dir = "tmp"

    def delete_tmp_dir(self):
        logger.info("Deleting the tmp directory if it is present")
        # Delete the tmp directory if it is present
        if os.path.exists(self.tmp_dir):
            shutil.rmtree(self.tmp_dir)

    def create_tmp_dir(self):
        logger.info("Creating a temporary directory if it doesn't exist")
        # Create a temporary directory if it doesn't exist
        if not os.path.exists(self.tmp_dir):
            os.makedirs(self.tmp_dir)

    def convert_to_csv(self, df, post_type):
        logger.info(f"Converting the given dataframe to csv and saving it in the tmp directory at path output_{post_type}.csv")
        # Convert the given dataframe to csv and save it in the tmp directory
        csv_path = os.path.join(self.tmp_dir, f"output_{post_type}.csv")
        df.to_csv(csv_path, index=False)
        logger.info(f"Dataframe converted to csv and saved in {csv_path}")


    def add_audit_fields_upload_to_s3(self):
        logger.info(f"Adding audit fields to the dataframe")

        for file_name in os.listdir(self.tmp_dir):
            if file_name.endswith(".csv"):
                csv_path = os.path.join(self.tmp_dir, file_name)
                post_type = file_name.split("_")[1].split(".")[0]
                print(f"post type is {post_type}")

                df = pd.read_csv(csv_path)

                df['audit_created_at'] = pd.Timestamp.now()
                df['audit_data_source'] = "reddit"
                df['audit_data_source_type'] = post_type

                parquet_path = os.path.join(self.tmp_dir, f"output_{post_type}.parquet")

                df.to_parquet(parquet_path, index=False)
                logger.info(f"Audit fields added to the dataframe and saved in {parquet_path}")

                now = pd.Timestamp.now()

                partition = f"year={now.year}/month={now.month}/day={now.day}/type={post_type}"
                s3_path = s3_credentials["s3_url"]
                s3_bucket = "prasad-reditt-test"
                s3_prefix = "bronze"
                s3_key = f"{s3_prefix}/{partition}/output_{post_type}.parquet"

                logger.info(f"Uploading the dataframe to S3 at path {s3_path}")

                s3_client = boto3.client(
                                        's3',
                                        aws_access_key_id=s3_credentials['aws_access_key_id'],
                                        aws_secret_access_key=s3_credentials['aws_secret_access_key']
                                        )

                s3_client.upload_file(parquet_path, s3_bucket, s3_key)

                logger.info(f"Dataframe uploaded to S3 at path {s3_path}")



