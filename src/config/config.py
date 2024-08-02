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
class DataIngestionConfig:
    raw_data_dir: str = os.path.join(DATA_DIR, RAW_DATA_DIR)
    raw_data_file_path = os.path.join(raw_data_dir, FILE_NAME)