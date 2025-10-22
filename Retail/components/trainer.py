from Retail.exception.exception import CustomException
from Retail.logging.logger import logging

import os,sys
import numpy as np
import pandas as pd

from Retail.entity.config_artifact import DataTransformationArtifact, ModelTrainerArtifact
from Retail.entity.entity_config import ModelTrainerConfig

from Retail.utils.main_utils.utils import save_numpy_obj,load_np_obj,evaluate_models,save_obj,import_obj
from Retail.utils.ml_utils.metric.classification_metric import get_classification_score
from Retail.utils.ml_utils.model.estimator import RetailModel 

from sklearn.linear_model import LinearRegression
from sklearn.metrics import accuracy_score
from sklearn.ensemble import (
    AdaBoostRegressor,
    GradientBoostingRegressor,
    RandomForestRegressor
)

import mlflow

import dagshub
dagshub.init(repo_owner='Rgarlay', repo_name='Mongodb', mlflow=True)


class ModelTrainer:
    def __init__(self, data_transformation_artifact: DataTransformationArtifact,
                 model_trainer_config: ModelTrainerConfig):
        try:
            logging.info("Initializing ModelTrainer...")
            self.data_transformation_artifact = data_transformation_artifact
            self.model_trainer_config = model_trainer_config
            logging.info("ModelTrainer initialized successfully.")
        except Exception as e:
            raise CustomException(e,sys)


    def track_mlflow(self, bestmodel,classification_metric):
        try:
            mlflow.set_tracking_uri("https://dagshub.com/Rgarlay/Mongodb.mlflow")
            with mlflow.start_run():
                mlflow.log_metric('r2_score',classification_metric.r2_score)
                mlflow.log_metric('rmse',classification_metric.root_mean_squared_error)
                mlflow.log_metric('mae',classification_metric.mean_absolute_error)
                #mlflow.sklearn.log_model(bestmodel,"model")
        except Exception as e:
            raise CustomException(e,sys)

    def train_model(self, x_train,x_test,y_train,y_test):
        try:

            logging.info("Starting model training process...")

            models = {
                'Random Forest': RandomForestRegressor(),
                'Gradient Boosting': GradientBoostingRegressor(),
                'Linear Regression': LinearRegression(),
                'AdaBoost': AdaBoostRegressor()
            }

            logging.info("Defined candidate models for training.")

            params = {
                "Random Forest": {
                    'n_estimators': [8, 16, 32, 128, 256]
                },
                "Gradient Boosting": {
                    'learning_rate': [0.1, 0.01, 0.05]
                },
                "Linear Regression": {
                    'fit_intercept': [True, False]
                },
                "AdaBoost": {
                    'n_estimators': [8, 16, 32, 64, 256]
                }
        }
            
            logging.info("Evaluating models with cross-validation and grid search...")
            model_report : dict = evaluate_models(x_train = x_train,
                                                    y_train=y_train,
                                                    x_test=x_test,
                                                    y_test=y_test,
                                                    models=models,
                                                    params=params)
            
            logging.info(f"Model evaluation completed. Report: {model_report}")

            best_model_score = max(sorted(model_report.values()))
            best_model_name = list(model_report.keys())[list(model_report.values()).index(best_model_score)]
            best_model = models[best_model_name]

            logging.info(f"Best model selected: {best_model_name} with score {best_model_score}")

            y_train_pred = best_model.predict(x_train)

            y_test_pred = best_model.predict(x_test)

        
            logging.info("Predictions generated for training and testing sets.")

            classification_train_metrics = get_classification_score(y_test=y_train, y_pred=y_train_pred)
            
            self.track_mlflow(bestmodel=best_model,classification_metric=classification_train_metrics)

            classification_test_metrics = get_classification_score(y_test=y_test, y_pred=y_test_pred)

            self.track_mlflow(bestmodel=best_model,classification_metric=classification_test_metrics)

            logging.info("Classification metrics calculated for train and test sets.")

            preprocessor = import_obj(self.data_transformation_artifact.transformed_obj_file_path)
            dirname = os.path.dirname(self.model_trainer_config.trained_model_file_path)
            os.makedirs(dirname,exist_ok=True)

            logging.info(f"Preprocessor imported successfully. Directory verified: {dirname}")

            retail_model = RetailModel(model=best_model, processor=preprocessor)
            save_obj(obj_to_save=retail_model, file_path=self.model_trainer_config.trained_model_file_path)

            logging.info(f"Combined RetailModel saved at {self.model_trainer_config.trained_model_file_path}")

            save_obj(file_path=r'final_obj/model.pkl',obj_to_save=best_model) ##saving model herer
            
            logging.info("Best model object saved separately at 'final_obj/model.pkl'")

            model_trainer_artifact = ModelTrainerArtifact(train_metric_artifact=classification_train_metrics,
                                                        test_metric_artifact=classification_test_metrics,
                                                        trained_model_file_path=self.model_trainer_config.trained_model_file_path)
            
            logging.info("ModelTrainerArtifact created successfully.")
            logging.info("Model training process completed.")


            return model_trainer_artifact
        except Exception as e:
            raise CustomException(e,sys)        



    def initiate_model_training(self):
        try:
            train_data_path = self.data_transformation_artifact.train_obj_file_path
            test_data_path = self.data_transformation_artifact.test_obj_file_path

            train_array = load_np_obj(train_data_path)
            test_array = load_np_obj(test_data_path)

            x_train,y_train,x_test,y_test = (
                train_array[:,:-1],
                train_array[:,-1],
                test_array[:,:-1],
                test_array[:,-1]
            )

            model_trainer_artifact = self.train_model(x_train=x_train,y_train=y_train,x_test=x_test,y_test=y_test)
            return model_trainer_artifact
        except Exception as e:
            raise CustomException(e,sys)