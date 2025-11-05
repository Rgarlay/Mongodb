from Retail.exception.exception import CustomException
from Retail.logging.logger import logging
import os,sys

import yaml
import numpy as np
import pickle
from sklearn.metrics import r2_score
from sklearn.model_selection import GridSearchCV

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
                yaml.dump(content,file)
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
    
def load_np_obj(file_path):
    try:
        with open(file_path, 'rb') as file:
            return np.load(file)
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
        with open(file_path,'rb') as file:
            return pickle.load(file)
    except Exception as e:
        raise CustomException(e,sys)
    

def evaluate_models(x_train,x_test,y_train,y_test,models,params) -> dict:
    try:
        report = {}

        for i in range(len(list(models))):
            model = list(models.values())[i]
            params = list(params.values())[i]

            gs = GridSearchCV(model,params,cv=3)
            gs.fit(x_train,y_train)

            model.set_params(**gs.best_params_)
            model.fit(x_train,y_train)

            y_train_pred = model.predict(x_train)
            y_test_pred = model.predict(x_test)


            train_accuracy_score = r2_score(y_train,y_train_pred)
            test_accuracy_score = r2_score(y_test,y_test_pred)

            report[list(models.keys())[i]] = test_accuracy_score

            return report
                           
    except Exception as e:
        raise CustomException(e,sys)
