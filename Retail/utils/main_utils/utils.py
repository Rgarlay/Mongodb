from Retail.exception.exception import CustomException
from Retail.logging.logger import logging
import os,sys

import yaml

def load_yaml_file(file_path):
    try:
        with open(file_path,'rb') as file:
            lines = yaml.safe_load(file)
            return lines
    except Exception as e:
        raise CustomException(e,sys)
    
def write_yaml_report(file_path: str, content: object, replace: bool=False):
    try:
        if replace:
            if os.path.exists(file_path):
                os.remove()
            os.makedirs(os.path.dirname(file_path),exist_ok=True)
            with open(file_path,'w') as file:
                file.dump(content,file)
    except Exception as e:
        raise CustomException(e,sys)
