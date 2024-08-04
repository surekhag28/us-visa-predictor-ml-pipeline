import os
from dataclasses import dataclass
from dotenv import load_dotenv
from src.constants import *


load_dotenv()

@dataclass
class DBConfig:
    HOST: str = os.getenv('DB_HOST')
    PORT: str = os.getenv('DB_PORT')
    NAME: str = os.getenv('DB_NAME')
    USER: str = os.getenv('DB_USER')
    PASSWORD: str = os.getenv('DB_PASSWORD')
    
@dataclass
class DataIngestionInput:
    raw_data_dir: str = os.path.join(DATA_DIR, RAW_DATA_DIR)
    raw_data_file_path:str = os.path.join(raw_data_dir, FILE_NAME)
    interim_dir:str = os.path.join(DATA_DIR, INTERIM_DATA_DIR)
    train_file_path:str = os.path.join(interim_dir, TRAIN_FILE)
    test_file_path:str = os.path.join(interim_dir, TEST_FILE)
    train_test_split_ratio:float = TRAIN_TEST_SPLIT_RATIO
    
@dataclass
class DataIngestionOutput:
    trained_file_path: str
    testing_file_path: str
    
@dataclass
class DataTransformationInput:
    processed_data_dir:str = os.path.join(DATA_DIR, PROCESSED_DATA_DIR)
    processed_train_file_path:str = os.path.join(processed_data_dir, PROCESSED_TRAIN_FILE)
    processed_test_file_path:str = os.path.join(processed_data_dir, PROCESSED_TEST_FILE)
    transformed_obj_file_path:str = os.path.join(MODEL_DIR, PREPROCESSING_OBJ_FILE)
    target_obj_file_path:str = os.path.join(MODEL_DIR, ENCODED_OBJ_FILE)
    
@dataclass
class DataTransformationOutput:
    processed_train_file_path:str
    processed_test_file_path:str
    processed_obj_file_path:str
    target_obj_file_path:str
    
@dataclass
class ModelTrainerInput:
    trained_model_file_path:str = os.path.join(MODEL_DIR, TRAINED_MODEL_FILE)
    expected_accuracy:float = MODEL_TRAINER_EXPECTED_SCORE
    
@dataclass
class ModelTrainerOutput:
    trained_model_file_path:str
    
@dataclass
class ModelEvaluationInput:
    pass

@dataclass
class ClassificationMetric:
    f1_score:float
    precision_score:float
    recall_score:float
    
@dataclass
class ModelEvaluationOutput:
    metrics:ClassificationMetric

    