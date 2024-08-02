import os
import datetime

DB_SCHEMA: str = 'visa_db'
DB_NAME: str = 'visadata'
FILE_NAME: str = 'Visadataset.csv'

# Data Ingestion related constants
DATA_DIR: str = 'data'
RAW_DATA_DIR: str = 'raw'
INTERIM_DATA_DIR:str = 'interim'

TRAIN_FILE: str = 'train.csv'
TEST_FILE: str = 'test.csv'
TRAIN_TEST_SPLIT_RATIO:float = 0.2

# Data transformation related constants
PROCESSED_DATA_DIR:str = 'processed'
PROCESSED_TRAIN_FILE:str = 'train_processed.csv'
PROCESSED_TEST_FILE:str = 'test_processed.csv'
PREPROCESSING_OBJ_FILE:str = 'preprocessor.pkl'
SCHEMA_FILE_PATH:str = os.path.join('config', 'schema.yaml')
