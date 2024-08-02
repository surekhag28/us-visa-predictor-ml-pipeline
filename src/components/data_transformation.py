import os
import sys
import pandas as pd
import numpy as np
from imblearn.combine import SMOTEENN
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder, OrdinalEncoder, PowerTransformer
from sklearn.compose import ColumnTransformer

from src.logger import logging as logger
from src.exception import *
from src.utils import read_yaml_file
from src.constants import SCHEMA_FILE_PATH
from src.data_access.usvisa_data import USvisaData
from src.config.config import (
                                    DataIngestionOutput,
                                    DataTransformationInput,
                                    DataTransformationOutput
                                )

class DataTransformation:
    
    def __init__(self, data_ingestion_output: DataIngestionOutput, 
                 data_transform_input: DataTransformationInput) -> None:
        
        self.data_ingestion_output = data_ingestion_output
        self.data_transform_input = data_transform_input
        self._schema_config = read_yaml_file(file_path=SCHEMA_FILE_PATH)
    
    def get_transformer_object(self) -> Pipeline:
        pass
        
        
    def run_data_transformation(self) -> DataTransformationOutput:
        pass