from tabula import read_pdf
import pandas as pd
import re
import numpy as np
import boto3
from io import StringIO
import logging

class DataExtraction:

    
    def get_data_from_santander(self, input_file, output_file):
        try:
            df_page = read_pdf(input_file, pages='all', multiple_tables=True, pandas_options={'header': None})
            combined_df = pd.concat(df_page, ignore_index=True)
            return combined_df.to_csv(output_file, index=False)
        except Exception as e:
            print(f"An error occurred: {e}")
