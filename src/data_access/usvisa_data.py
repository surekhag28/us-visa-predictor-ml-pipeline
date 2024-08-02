import sys
import pandas as pd
import numpy as np
from src.logger import logging as logger
from src.db.db_connector import DatabaseConnection
from src.exception import DatabaseConnectionError
from src.config.config import DB_SCHEMA, DB_NAME

class USvisaData:
    
    def __init__(self):
        db_connector = DatabaseConnection()
        try:
            self.connection = db_connector.get_connection()
        except Exception as e:
            logger.error('Failed to establish connection with the database: {}'.format(e))
            raise DatabaseConnectionError(e, sys)
    
    def export_data_as_dataframe(self):
        
        try:
            query = 'SELECT * from ' + DB_SCHEMA + '.' + DB_NAME
            cursor = self.connection.cursor()
            cursor.execute(query)
            data = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
        except Exception as e:
            logger.error('Failed to establish connection with the database')
            raise DatabaseConnectionError(e, sys)
        finally:
            if cursor:
                cursor.close
            if self.connection:
                self.connection.close()
                
        usvisa_df = pd.DataFrame(data, columns=columns)
        return usvisa_df
            

# for testing purpose
""" if __name__=='__main__':
    obj = USvisaData()
    data = obj.export_data_as_dataframe()
    print(data.head(5))  """