import os
import sys
import pandas as pd
import numpy as np
from imblearn.combine import SMOTEENN
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import (
                                    StandardScaler, 
                                    OneHotEncoder, 
                                    OrdinalEncoder, 
                                    PowerTransformer,
                                    LabelEncoder
                                )
from sklearn.compose import ColumnTransformer

from src.logger import logging as logger
from src.exception import *
from src.constants import CURRENT_YEAR, TARGET_COLUMN
from src.utils import read_yaml_file, save_object, save_numpy_array
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
        try:
            numeric_transformer = StandardScaler()
            oh_transformer = OneHotEncoder()
            or_transformer = OrdinalEncoder()
            
            logger.info("Initialised standardscaler, onehotencoder and ordinalencoder")
            
            oh_columns = self._schema_config['oh_columns']
            or_columns = self._schema_config['or_columns']
            transform_columns = self._schema_config['transform_columns']
            num_features = self._schema_config['num_features']
            
            logger.info("Got columns for transformation from the schema file")
            
            transform_pipe = Pipeline(steps=[
                            ('transformer', PowerTransformer(method='yeo-johnson'))
                        ])
            
            logger.info("Initialised power transformer")
            
            preprocessor = ColumnTransformer([
                    ('OneHotEncoder', oh_transformer, oh_columns),
                    ('OrdinalEncoder', or_transformer, or_columns),
                    ('Transformer', transform_pipe, transform_columns),
                    ('StandardScaler', numeric_transformer, num_features)
                ])
            
            logger.info('Created processor object')
            
            return preprocessor
        except Exception as e:
            raise USvisaException(e, sys)
        
    def run_data_transformation(self) -> DataTransformationOutput:
        try:
            logger.info("Data transformation initiated")
            
            preprocessor = self.get_transformer_object()
            logger.info("Got the preprocessor object")
            
            drop_columns = self._schema_config['drop_columns']
            
            train_df = pd.read_csv(self.data_ingestion_output.trained_file_path)
            train_df['company_age'] = CURRENT_YEAR - train_df['yr_of_estab']
            
            test_df = pd.read_csv(self.data_ingestion_output.testing_file_path)
            test_df['company_age'] = CURRENT_YEAR - test_df['yr_of_estab']
            logger.info('Created new feature for both train and test data')
            
            input_feature_train_df = train_df.drop(columns=drop_columns, axis=1)
            target_feature_train_df = train_df[TARGET_COLUMN]
            
            input_feature_test_df = train_df.drop(columns=drop_columns, axis=1)
            target_feature_test_df = train_df[TARGET_COLUMN]
            logger.info('Dropped unnecessary columns form both train and test data')
            
            
            target_encoder = LabelEncoder()
            target_feature_train_arr = target_encoder.fit_transform(target_feature_train_df)
            target_feature_test_arr = target_encoder.transform(target_feature_test_df)
            logger.info("Encoded target feature for both train and test data")
            
            input_feature_train_arr = preprocessor.fit_transform(input_feature_train_df)
            input_feature_test_arr = preprocessor.transform(input_feature_test_df)
            logger.info("Transformed input features for both train and test data")
            
            # Smoting only needs to be applied on training data to avoid data leakage for testing data and to avoid biased predictions.
            smt = SMOTEENN(sampling_strategy='minority')
            
            input_feature_train_final, target_feature_train_final = smt.fit_resample(
                input_feature_train_arr, target_feature_train_arr
            )
            logger.info("Applied SMOTTEN on train data")
            
            train_arr = np.c_[input_feature_train_arr, target_feature_train_arr]
            test_arr = np.c_[input_feature_test_arr, target_feature_test_arr]
            
            # save objects and data for further access during model training
            save_object(self.data_transform_input.transformed_obj_file_path, preprocessor)
            save_object(self.data_transform_input.target_obj_file_path, target_encoder)
            save_numpy_array(self.data_transform_input.processed_train_file_path, train_arr)
            save_numpy_array(self.data_transform_input.processed_test_file_path, test_arr)
            
            logger.info('Saved the preprocessor object and processed train and test data')
            logger.info("Exited data transformation")
            
            data_transformation_output = DataTransformationOutput(
                self.data_transform_input.processed_train_file_path,
                self.data_transform_input.processed_test_file_path,
                self.data_transform_input.transformed_obj_file_path,
                self.data_transform_input.target_obj_file_path
            )
            
            return data_transformation_output
        except Exception as e:
            raise USvisaException(e, sys)