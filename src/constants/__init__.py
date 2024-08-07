import os
from datetime import date

DB_SCHEMA: str = 'visa_db'
DB_NAME: str = 'visadata'
FILE_NAME: str = 'Visadataset.csv'
TARGET_COLUMN = 'case_status'
CURRENT_YEAR = date.today().year

# Data Ingestion related constants
DATA_DIR: str = 'data'
RAW_DATA_DIR: str = 'raw'
INTERIM_DATA_DIR:str = 'interim'

TRAIN_FILE: str = 'train.csv'
TEST_FILE: str = 'test.csv'
TRAIN_TEST_SPLIT_RATIO:float = 0.2

# Data transformation related constants
MODEL_DIR = 'models'
PROCESSED_DATA_DIR:str = 'processed'
PROCESSED_TRAIN_FILE:str = 'train_processed.npy'
PROCESSED_TEST_FILE:str = 'test_processed.npy'
PREPROCESSING_OBJ_FILE:str = 'preprocessor.pkl'
ENCODED_OBJ_FILE:str = 'targetencoder.pkl'
SCHEMA_FILE_PATH:str = os.path.join('config', 'schema.yaml')

# Model training related constants
TRAINED_MODEL_FILE: str = 'model.pkl'
MODEL_TRAINER_EXPECTED_SCORE:float = 0.6

MLFLOW_TRACKING_URI:str = 'http://localhost:8080'
METRICS_DIR: str = 'metrics'