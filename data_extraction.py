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
            df_page2 = read_pdf(input_file, pages=2, area=[399.99, 0, 842, 595], multiple_tables=True, pandas_options={'header': None})
            df_page3 = read_pdf(input_file, pages=3, multiple_tables=True, pandas_options={'header': None})
            df_page4 = read_pdf(input_file, pages=4, multiple_tables=True, pandas_options={'header': None})
            if df_page4 is not None:
                all_tables1 = df_page2 + df_page3 + df_page4
                combined_df1 = pd.concat(all_tables1, ignore_index=True)
                return combined_df1.to_csv(output_file, index=False)
            all_tables = df_page2 + df_page3
            combined_df = pd.concat(all_tables, ignore_index=True)
            return combined_df.to_csv(output_file, index=False)
        except Exception as e:
            print(f"An error occurred: {e}")
