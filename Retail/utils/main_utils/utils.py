from Retail.exception.exception import CustomException
from Retail.logging.logger import logging
import os,sys

import yaml
import numpy as np
import pickle
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


def save_numpy_obj(object_to_save,file_path):
    try:
        dir_name = os.path.dirname(file_path)
        os.makedirs(dir_name,exist_ok=True)
        with open(file_path, 'wb') as file:
            np.save(file, object_to_save)
    except Exception as e:
        raise CustomException(e,sys)
    

def save_obj(obj_to_save, file_path):
    try:
        dir_name = os.path.dirname(file_path)
        os.makedirs(dir_name,exist_ok=True)
        with open(file_path, 'wb') as file:
            pickle.dump(obj_to_save,file)
    except Exception as e:
        raise CustomException(e,sys)
    
def import_obj(file_path):
    try:
        if not os.path.dirname(file_path):
            raise Exception(f'The file at the location {file_path} does not exist.')
        with open(file_path,'w') as file:
            pickle.load(file)
    except Exception as e:
        raise CustomException(e,sys)
    