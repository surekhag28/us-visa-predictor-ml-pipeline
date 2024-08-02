import os
import sys
import pandas as pd
from src.constants import DB_SCHEMA, DB_NAME
from src.logger import logging as logger
from src.config.config import DataIngestionConfig
from src.db.db_connector import DatabaseConnection
from src.exception import DatabaseConnectionError


def create_db_schema(sql_file_path):
    
    """
    Creates a schema in the PostgreSQL database using a SQL script.

    Parameters:
        sql_file_path (str): Path to the SQL script file.
        global_conn (str): DB connection string.
    """
    db_connector = DatabaseConnection()
    
    try:
        conn = db_connector.get_connection()
        cursor = conn.cursor()
        
        with open(sql_file_path, 'r') as file:
            sql_script = file.read()
        
        cursor.execute(sql_script)
        conn.commit()
        
    except FileNotFoundError as e:
        logger.error('Unable to find sql file at location: %s', sql_file_path)
        raise
    except Exception as e:
        logger.error('Database connection error')
        raise DatabaseConnectionError(e, sys)

    finally:
        if cursor:
            cursor.close()
        if conn:
            db_connector.close_connection()
            
def load_data(file_path):
    
    """
    Ingests data into table from csv file.

    Parameters:
        file_path (str): Path to the raw CSV data file.
    """
    
    df = pd.read_csv(file_path)
    data = df.values.tolist()
    
    sql01 = "INSERT INTO " + DB_SCHEMA + "." + DB_NAME + "(case_id, continent, education_of_employee, \
                    has_job_experience, requires_job_training, no_of_employees, yr_of_estab, \
                    region_of_employment, prevailing_wage, unit_of_wage, full_time_position, case_status)\
                    VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    
    db_connector = DatabaseConnection()
    
    try:         
        conn = db_connector.get_connection()
        
        cur = conn.cursor()
        del_statement = "DELETE FROM " + DB_SCHEMA + "." + DB_NAME
        cur.execute(del_statement,)
        cur.executemany(sql01,data)
        conn.commit()
        conn.close()
    except Exception as e:
        logger.error('Database connection error')
        raise DatabaseConnectionError(e, sys)
    finally:
        if conn is not None:
            db_connector.close_connection()
            
if __name__=='__main__':
    
    create_db_schema(os.path.join(os.path.dirname(__file__), 'db_schema.sql'))
    logger.info('Database created')
    
    load_data(DataIngestionConfig.raw_data_file_path)
    logger.info('Data ingested into table')
    