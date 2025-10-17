import sys, os
import numpy as np
import pandas as pd
from sklearn.impute import KNNImputer   
from sklearn.pipeline import Pipeline

from Retail.exception.exception import CustomException
from Retail.logging.logger import logging

from Retail.constants.training_pipeline import TARGET_COLUMN,DATA_TRANSFORMATION_IMPUTE_PARAMS
from Retail.constants.training_pipeline import DATA_TRANSFORMATION_IMPUTE_PARAMS, GENDER_COLUMN_TO_MAP, CATEGORICAL_COL_TO_OHE
from Retail.constants.training_pipeline import  CATEGORICAL_COL_TO_OHE

from Retail.entity.config_artifact import DataTransformationArtifact,DataValidationArtifact
from Retail.entity.entity_config import DataTransformationConfig
from Retail.utils.main_utils.utils import save_numpy_obj, save_obj

class DataTransformation:
    def __init__(self, data_validation_artifact: DataValidationArtifact,
                 data_transformation_config:DataTransformationConfig):
        try:
            self.data_validation_artifact = data_validation_artifact
            self.data_transformation_config = data_transformation_config
        except Exception as e:
            raise CustomException(e,sys)
        
    @staticmethod
    def import_csv_file(file_path):
        try:
            df =  pd.read_csv(file_path)
            logging.info(f"CSV file loaded successfully with shape: {df.shape}")
            return df
        except Exception as e:
            raise CustomException(e,sys)
        
    def get_data_transformer(dataframe):
        try:

            ##Numerical transformations
            Knn_imputer = KNNImputer(**DATA_TRANSFORMATION_IMPUTE_PARAMS)
            processor = Pipeline([('imputer',Knn_imputer)])
            logging.info("KNNImputer pipeline created successfully.")
            return processor
        except Exception as e:
            raise CustomException(e,sys)
        
    def initiate_data_transformation(self):
        try:
            train_data = DataTransformation.import_csv_file(self.data_validation_artifact.valid_train_file_path)
            test_data = DataTransformation.import_csv_file(self.data_validation_artifact.valid_test_file_path)

            logging.info(f'The columns in train_data are {train_data.columns}')
            logging.info(f'The columns in train_data are {test_data.columns}')

            ## Did the mapping of Gender as Male -> 1; Female -> 0.
            logging.info("Mapping gender column: Male -> 1, Female -> 0")
            train_data['is_male'] = train_data['is_male'].apply(lambda x: 1 if x == 'Male' else 0)
            test_data['is_male'] = test_data['is_male'].apply(lambda x: 1 if x=='Male' else 0)

            ##Doing the imputations

                ##Splitting numerical columns
            logging.info("Selecting numerical columns for imputation...")    
            train_data_numerical = train_data.select_dtypes(include = 'number')
            test_data_numerical = test_data.select_dtypes(include = 'number')

                ## applying knninputer onto it.
            logging.info("Applying KNN imputer to numerical columns...")
            preprocessor = self.get_data_transformer()
            preprocessor_obj = preprocessor.fit(train_data_numerical)

            transformed_train_data_np = preprocessor_obj.transform(train_data_numerical)
            transformed_train_data = pd.DataFrame(transformed_train_data_np,columns=train_data_numerical.columns)

            transformed_test_data_np = preprocessor_obj.transform(test_data_numerical)
            transformed_test_data = pd.DataFrame(transformed_test_data_np,columns=test_data_numerical.columns)
            logging.info("Transformed numerical data converted back to DataFrame.")

            ##Performing the categorical transformation
            logging.info(f"Performing One-Hot Encoding on columns: {CATEGORICAL_COL_TO_OHE}")
            train_data_obj = train_data[CATEGORICAL_COL_TO_OHE]
            test_data_obj = test_data[CATEGORICAL_COL_TO_OHE]

            train_data_OHE = pd.get_dummies(data =train_data_obj, 
                                            columns=[CATEGORICAL_COL_TO_OHE],
                                              dtype = int, drop_first=True)
            
            test_data_OHE = pd.get_dummies(data =test_data_obj, 
                                            columns=[CATEGORICAL_COL_TO_OHE],
                                              dtype = int, drop_first=True)

            input_train_data_transformed = pd.concat([transformed_train_data,train_data_OHE], axis = 1)
            input_test_data_transformed = pd.concat([transformed_test_data,test_data_OHE], axis = 1)
            logging.info(f"Transformed train shape: {input_train_data_transformed.shape}, "
                         f"test shape: {input_test_data_transformed.shape}")
            
            ##Splitted the train-test data column speperately.
            input_feature_train_df = input_train_data_transformed.drop(columns= [TARGET_COLUMN])
            input_target_target_df = input_train_data_transformed[TARGET_COLUMN]
            
            input_feature_test_df = input_test_data_transformed.drop(columns= [TARGET_COLUMN])
            input_target_test_df = input_test_data_transformed[TARGET_COLUMN]

            logging.info(f'test train feature == {input_feature_train_df.columns}')
            logging.info(f'test test feature == {input_feature_test_df.columns}')

            train_arr=np.c_[input_feature_train_df.to_numpy(),np.array(input_target_target_df)]
            test_arr=np.c_[input_feature_test_df.to_numpy(),np.array(input_target_test_df)]
            logging.info(f"Final NumPy arrays created: Train shape {train_arr.shape}, Test shape {test_arr.shape}")

            save_numpy_obj(object_to_save=train_arr, file_path=self.data_transformation_config.transformed_train_file_path)
            save_numpy_obj(object_to_save=test_arr, file_path=self.data_transformation_config.transformed_test_file_path)
            save_obj(obj_to_save=preprocessor, file_path=self.data_transformation_config.trained_obj_file_path)
            
            data_tranformation_artifact = DataTransformationArtifact(transformed_obj_file_path=self.data_transformation_config.trained_obj_file_path,
                                                                    train_obj_file_path=self.data_transformation_config.transformed_train_file_path,
                                                                    test_obj_file_path=self.data_transformation_config.transformed_test_file_path)
            logging.info("All transformed data and objects saved successfully.")
            
            return data_tranformation_artifact
        
        except Exception as e:
            raise CustomException(e,sys)