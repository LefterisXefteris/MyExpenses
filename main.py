from tabula import read_pdf
import pandas as pd
import re
import numpy as np


class Santander:

    
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

        




if __name__ == '__main__':
    sa = Santander()
    dc = DataCleaning()


    table1 = sa.get_data_from_santander('file1.pdf', 'o2.csv')
    table = pd.read_csv('o2.csv')
    table2 = dc.clean_santander_data(table)
    table2.to_csv('cleaned_data_test.csv', index=True)
    print(table2.head(50))
    

    


    
    

