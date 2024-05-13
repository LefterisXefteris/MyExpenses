
from tabula import read_pdf
import pandas as pd
import re
import numpy as np
import boto3
from io import StringIO
import logging






class uploadDataToS3:


    def __init__(self, aws_access_key_id, aws_secret_access_key, region_name):
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=region_name
        )
    

    def convert_dataframe_to_csv_and_upload(self, df, bucket_name, object_name):
            # Create a buffer
            csv_buffer = StringIO()
            df.to_csv(csv_buffer, index=False)

            # Reset the buffer position to the beginning
            csv_buffer.seek(0)

            # Upload the DataFrame from the buffer to S3
            try:
                self.s3_client.put_object(
                    Bucket=bucket_name,
                    Key=object_name,
                    Body=csv_buffer.getvalue()
                )
                logging.info(f'Successfully uploaded {object_name} to bucket {bucket_name}.')
            except Exception as e:
                logging.error(f'Failed to upload {object_name} to bucket {bucket_name}: {e}')

