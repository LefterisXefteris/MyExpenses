import psycopg2
import sqlalchemy
import yaml 
from sqlalchemy import Engine, create_engine, engine_from_config, text, inspect, bindparam
import pandas as pd

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


    def init_db_engine(self, creds):

        HOST = creds['RDS_HOST']
        USER = creds['RDS_USER']
        PASSWORD = creds['RDS_PASSWORD']
        DATABASE = creds['RDS_DATABASE']
        PORT = creds['RDS_PORT']
        DATABASE_TYPE = 'postgresql'
        DBAPI = 'psycopg2'

        self.engine = create_engine(f"{DATABASE_TYPE}+{DBAPI}://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}")

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
            df = pd.DataFrame(df).reset_index()  # Reset the index to include it as a column
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




        
   