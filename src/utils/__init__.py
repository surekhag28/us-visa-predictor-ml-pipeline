import os
import sys
import dill
import yaml
import numpy as np
from src.exception import USvisaException
from src.logger import logging as logger

def read_yaml_file(file_path:str) -> None:
    try:
        with open(file_path, 'rb') as f:
            return yaml.safe_load(f)
    except Exception as e:
        raise USvisaException(e, sys)
    
def save_object(file_path:str, obj:object) -> None:
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'wb') as file_obj:
            dill.dump(obj, file_obj)
        
        logger.info("Saved the object in file and exit the process")
    except Exception as e:
        raise USvisaException(e, sys)
    
def save_numpy_array(file_path:str, array:np.array) -> None:
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'wb') as file_obj:
            np.save(file_obj, array)
            
        logger.info('Saved processed data in file and exit the process')
    except Exception as e:
        raise USvisaException(e, sys)
    
def load_numpy_array(file_path:str) -> None:
    try:
        with open(file_path, 'rb') as file_obj:
            return np.load(file_obj)
    except Exception as e:
        raise USvisaException(e, sys)