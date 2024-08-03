import os
import sys
import pandas as pd
import numpy as np
from src.logger import logging as logger
from src.exception import *
from src.config.config import *
from src.components.data_ingestion import DataIngestion
from src.components.data_transformation import DataTransformation

class TrainingPipeline:
    def __init__(self):
        self.data_ingestion_input = DataIngestionInput()
        self.data_transformation_input = DataTransformationInput()
    
    def run_training_pipeline(self):
        # data ingestion process - train test split
        data_ingestion = DataIngestion(self.data_ingestion_input)
        data_ingestion_output = data_ingestion.run_data_ingestion()
        
        # data transformation process
        data_transformation = DataTransformation(data_ingestion_output, self.data_transformation_input)
        data_transformation_output = data_transformation.run_data_transformation()
        
if __name__=="__main__":
    pipeline = TrainingPipeline()
    pipeline.run_training_pipeline()
    