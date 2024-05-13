from tabula import read_pdf
import pandas as pd
import re
import numpy as np
import boto3
from io import StringIO
import logging
from data_cleaning import DataCleaning
from data_extraction import DataExtraction
from uploadDataToS3 import uploadDataToS3


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    aws_access_key_id = 'AKIA435ULAGV54PPKQAC'
    aws_secret_access_key = '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'
    region_name = 'eu-west-1'


    data_extractor = DataExtraction()
    data_cleaner = DataCleaning()


    raw_data_csv = 'output.csv'  
    table1 = data_extractor.get_data_from_santander('file1.pdf', raw_data_csv)
    table = pd.read_csv(raw_data_csv)
    cleaned_data = data_cleaner.clean_santander_data(table)
    print(cleaned_data.head(50))


    uploader = uploadDataToS3(aws_access_key_id, aws_secret_access_key, region_name)
    bucket_name = 'financialdatabucket'  
    object_name = 'cleaned_data_test.csv'
    uploader.convert_dataframe_to_csv_and_upload(cleaned_data, bucket_name, object_name)


    

    


    
    

