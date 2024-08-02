import yaml
from src.exception import USvisaException

def read_yaml_file(file_path:str) -> None:
    try:
        with open(file_path, 'rb') as f:
            return yaml.safe_load(f)
    except Exception as e:
        raise USvisaException(e, sys)