import os
import sys
import psycopg2
import logging
import pandas as pd
from src.constants import *
from src.config.config import DBConfig, DataIngestionConfig

logger = logging.getLogger(__name__)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(name)50s:%(lineno)4s - %(funcName)25s() ] - ( %(levelname)5s ) %(message)s",
    handlers=[logging.FileHandler("create_schema.log"), logging.StreamHandler(sys.stdout)],
)

def create_db_schema(sql_file_path, global_conn):
    
    """
    Creates a schema in the PostgreSQL database using a SQL script.

    Parameters:
        sql_file_path (str): Path to the SQL script file.
        global_conn (str): DB connection string.
    """
    
    try:
        conn = psycopg2.connect(global_conn)
        cursor = conn.cursor()
        
        with open(sql_file_path, 'r') as file:
            sql_script = file.read()
        
        cursor.execute(sql_script)
        conn.commit()

    except FileNotFoundError as e:
        logger.error('Unable to find sql file at location: %s', sql_file_path)
        raise
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        raise

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
            
def load_data(file_path):
    df = pd.read_csv(file_path)
    data = df.values.tolist()
    
    sql01 = "INSERT INTO " + DB_SCHEMA + ".visadata(case_id, continent, education_of_employee, \
                    has_job_experience, requires_job_training, no_of_employees, yr_of_estab, \
                    region_of_employment, prevailing_wage, unit_of_wage, full_time_position, case_status)\
                    VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    conn = None
    try:         
        conn = psycopg2.connect(global_conn)
        
        cur = conn.cursor()
        del_statement = "DELETE FROM " + DB_SCHEMA + ".visadata"
        cur.execute(del_statement,)
        cur.executemany(sql01,data)
        conn.commit()
        conn.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            
if __name__=='__main__':
    
    global_conn = f'host={DBConfig.HOST} port={DBConfig.PORT} dbname={DBConfig.NAME} user={DBConfig.USER} password={DBConfig.PASSWORD}'
    create_db_schema(os.path.join(os.path.dirname(__file__), 'db_schema.sql'), global_conn)
    logger.info('Database created')
    
    load_data(DataIngestionConfig.raw_data_file_path)
    logger.info('Data ingested into table')
    