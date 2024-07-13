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
        df = df[1:] 
        df.columns = ['Date', 'Description', 'Money in', 'Money out', 'Balance']
        df['Description'] = df['Description'].str.cat(df['Money out'], sep=' ')
        df = df.dropna(thresh=2)
        df = df.drop_duplicates()
        df = df.fillna(0)
        df['Money in'] = pd.to_numeric(df['Money in'].str.replace('£', '').str.replace(',', '').str.strip(), errors='coerce').fillna(0)
        df['Money out'] = pd.to_numeric(df['Money out'].str.replace('£', '').str.replace(',', '').str.strip(), errors='coerce').fillna(0)
        df['Description'] = df['Description'].astype(str)
        df.drop('Balance', axis=1, inplace=True)
        return df

    def clean_santander_data_for_postgres(self, table):
        df = pd.DataFrame(table)
        df.drop(['Category'], axis=1, inplace=True)
        df = df.rename(columns={'Predicted Category':'Category'})
        df = df.reset_index(drop=True)
        return df
    
    def concat_and_sort_df_bydate(self, *args):
        concatenated_df = pd.concat(args, ignore_index=True)
        sorted_df = concatenated_df.sort_values('Date')
        return sorted_df
    
