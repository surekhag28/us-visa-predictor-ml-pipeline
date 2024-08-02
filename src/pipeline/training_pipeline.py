import os
import sys
import pandas as pd
import numpy as np
from src.logger import logging as logger
from src.exception import *
from src.config.config import *
from src.components.data_ingestion import DataIngestion

class TrainingPipeline:
    def __init__(self):
        self.data_ingestion_config = DataIngestionInput()
    
    def run_training_pipeline(self):
        # data ingestion process - train test split
        data_ingestion = DataIngestion(self.data_ingestion_config)
        data_ingestion_output = data_ingestion.run_data_ingestion()
        
if __name__=="__main__":
    pipeline = TrainingPipeline()
    pipeline.run_training_pipeline()