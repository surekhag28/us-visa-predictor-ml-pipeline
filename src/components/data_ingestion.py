import os
import sys
import pandas as pd
import numpy as np
from src.logger import logging as logger
from src.exception import *
from src.data_access.usvisa_data import USvisaData
from src.config.config import DataIngestionInput,DataIngestionOutput
from sklearn.model_selection import train_test_split

class DataIngestion:
    """
        :param data_ingestion_config: configuration for data ingestion
    """
        
    def __init__(self, data_ingestion_config: DataIngestionInput) -> None:
        self.data_ingestion_input = data_ingestion_config
    
    
    def split_train_test_data(self):
        
        """
        Splits the data into train and test data.

        Output: train and test data are stored in data directory
        On Failure: Raises exception
        """
        try:
            visadata = USvisaData()
            df = visadata.export_data_as_dataframe()
            train_data, test_data = train_test_split(df, test_size=self.data_ingestion_input.train_test_split_ratio, random_state=42)
            logger.info("Train test split performed on the dataset")
            dir_path = os.path.dirname(self.data_ingestion_input.train_file_path)
            os.makedirs(dir_path, exist_ok=True)
            
            logger.info('Exporting train and test data into csv files')
            
            train_data.to_csv(self.data_ingestion_input.train_file_path, index=False, header=True)
            test_data.to_csv(self.data_ingestion_input.test_file_path, index=False, header=True)
            logger.info('Train and test data files exported to csv')
        except Exception as e:
            logger.error('Some error occurred')
            raise USvisaException(e, sys)
        
    
    def run_data_ingestion(self) -> DataIngestionOutput:
        
        """
        This method initiates the data ingestion component of training pipeline.
        
        Output: train and test data file paths are returned as output
        On Failure: Raises exception

        """
        try:
            logger.info("Initiated data ingestion process")
            self.split_train_test_data()
            data_ingestion_output = DataIngestionOutput(trained_file_path=self.data_ingestion_input.train_file_path,
                                                        testing_file_path=self.data_ingestion_input.test_file_path)
            
            logger.info("Data Ingestion completed")
            logger.info("Data Ingestion output: {}".format(data_ingestion_output))
            
            return DataIngestionOutput
        except Exception as e:
            raise USvisaException(e, sys)