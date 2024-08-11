import os
import sys
import mlflow
import pandas as pd
import numpy as np


from src.logger import logging as logger
from src.exception import USvisaException
from src.utils import load_object, read_yaml_file
from src.constants import SCHEMA_FILE_PATH, CURRENT_YEAR
from src.config.config import PredictionInput


class PredictionPipeline:
    def __init__(self) -> None:
        self.prediction_input = PredictionInput()
        self._schema_config = read_yaml_file(file_path=SCHEMA_FILE_PATH)
        
    def predict(self, transformed_arr: np.ndarray) -> None:
        try:
            model = load_object(self.prediction_input.trained_model_file_path)
            
            targetencoder = load_object(self.prediction_input.targetencoder_file_path)
            targets = model.predict(transformed_arr).astype(int)
            predictions = targetencoder.inverse_transform(targets)
            logger.info(predictions)
            
        except Exception as e:
            raise USvisaException(e, sys)
    
    def preprocess(self, data: pd.DataFrame) -> np.ndarray:
        try:
            schema_columns = self._schema_config['columns']
            columns = []
            for item in schema_columns:
                columns.extend(item.keys())
            
            drop_columns = self._schema_config['drop_columns']
            
            preprocessor = load_object(self.prediction_input.preprocessor_file_path)
            data.columns = columns[:-1]
            
            data['company_age'] = CURRENT_YEAR - data['yr_of_estab']
            data = data.drop(columns=drop_columns, axis=1)
            
            transformed_data = preprocessor.transform(data)
            logger.info("Transformed the prediction data")
            
            return transformed_data
        except Exception as e:
            raise USvisaException(e, sys)
        
        
    def run_prediction_pipeline(self):
        try:
            logger.info("Started inference pipeline")
            
            data = pd.read_csv(self.prediction_input.prediction_file_path)
            
            transformed_data = self.preprocess(data)
        
            predictions = self.predict(transformed_data)
            logger.info(predictions)
        except Exception as e:
            raise USvisaException(e, sys)
        
        
        
if __name__=="__main__":
    prediction_pipeline = PredictionPipeline()
    prediction_pipeline.run_prediction_pipeline()
        