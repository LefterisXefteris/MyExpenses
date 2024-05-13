from tabula import read_pdf
import pandas as pd
import re
import numpy as np
import boto3
from io import StringIO
import logging


class DataCleaning:

    
    def clean_santander_data(self, table):
        df = pd.DataFrame(table)
        df = df[3:] 
        df.columns = ['Date', 'Description', 'Money in', 'Money out', 'Balance']
        df['Money in'] = df['Description']  
        df['Description'] = df['Date'].str.extract(r'(\d+\w+ \w+ [A-Z]+[^\d]+)') 
        df['Date'] = df['Date'].str.extract(r'(\d+\w+ \w+)')
        rows_to_drop = [31] 
        df.drop(index=rows_to_drop, inplace=True)
        condition = df['Money in'].apply(lambda x: isinstance(x, str) and x.isdigit() == False)
        df.loc[condition, 'Description'] = df.loc[condition, 'Money in']
        df.loc[condition, 'Money in'] = np.nan
        df['Money in'] = pd.to_numeric(df['Money in'], errors='coerce')
       
        return df