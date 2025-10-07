import yaml
from Retail.exception.exception import CustomException
from Retail.logging.logger import logging
import os,sys
import numpy as np
import dill
import pickle


def read_yaml_file(file_path:str) -> dict:
    try:
        with open(file_path,'rb') as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise CustomException(e,sys)
    
def write_ymal_file(file_path:str, content: object, replace: bool = False) -> None:
    try:
        if replace:
            ##if path exists, remove it
            if os.path.exists(file_path):
                os.remove(file_path)
            ##made a new folder with a file_path 
            os.makedirs(os.path.filename(file_path), exist_ok=True)

            ##dumped our content there
            with open(file_path,'w') as file:
                yaml.dump(content,file)
    except Exception as e:
        raise CustomException(e,sys)