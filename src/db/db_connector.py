import psycopg2
from psycopg2 import OperationalError
from src.config.config import *
from src.logger import logging as logger

class DatabaseConnection:
    def __init__(self):
        self.__connection = None
        
    def __connect(self):
        """
        Establishes a connection to the PostgresSQL database.
        
        Returns:
            bool: True if the connection is successful, False otherwise
        """
        
        try:
            self.__connection = psycopg2.connect(
                                    host = DBConfig.HOST,
                                    port = DBConfig.PORT,
                                    user = DBConfig.USER,
                                    password = DBConfig.PASSWORD,
                                    database = DBConfig.NAME
                                )
            
            return True
        except OperationalError as e:
            logger.error('Error connecting to the database: {}'.format(e)) 
            return False
        
    def get_connection(self):
        if self.__connection is None:
            if not self.__connect():
                raise Exception('Failed to establish database connection')
        return self.__connection
        
    def close_connection(self):
        if self.__connection:
            try:
                self.__connection.close()
                self.__connection = None
                logger.info('Database connection closed')
            except Exception as e:
                logger.error('Error closing the database connection: {}'.format(e))   
            
        