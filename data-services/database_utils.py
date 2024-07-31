import psycopg2
import sqlalchemy
import yaml 
from sqlalchemy import Engine, create_engine, engine_from_config, text, inspect, bindparam
import pandas as pd
import os
class DatabaseUtills:
    def __init__(self):
        self.engine = None

    def read_db_creds(self, file):
        try:
            with open(file) as f:
                creds = yaml.safe_load(f)
            return creds
        except:
            print("Failed to read cred")



    def init_db_engine(self):
        DATABASE_URL = os.getenv('SQLALCHEMY_DATABASE_URI')
        if not DATABASE_URL:
            raise ValueError("Database URL not set in environment variables")
        
        self.engine = create_engine(DATABASE_URL)
        return self.engine
    
    def list_db_tables(self, engine):
        try:
            with engine.connect() as connection:
                result = connection.execute(text("""SELECT table_name FROM information_schema.tables
       WHERE table_schema = 'public'"""))
                for row in result:
                    print(row)
        except Exception as e:
            print("Failed to fecth tables.", e)


    def upload_to_db(self, df, table_name):
        try:
            df = pd.DataFrame(df).reset_index() 
            data = df.to_dict(orient='records')
            with self.engine.connect() as conn:
                for row in data:
                    stmt = text(f"""
                        INSERT INTO {table_name} (index, categoryname)
                        VALUES (:index, :categoryname)
                        ON CONFLICT (index) DO UPDATE SET
                        categoryname = EXCLUDED.categoryname
                    """)
                    conn.execute(stmt, {'index': row['index'], 'categoryname': row['categoryname']})
            
            print("Table uploaded")
        except Exception as e:
            print('Failed to upload pandas category dataframe to postgres sql table', e)




        
   