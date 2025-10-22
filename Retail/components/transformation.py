import sys, os
import numpy as np
import pandas as pd
from sklearn.impute import KNNImputer   
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer

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
        
    def get_data_transformer(cls):
        try:
            ##Numerical transformations
            num_imputer = KNNImputer(**DATA_TRANSFORMATION_IMPUTE_PARAMS)
            num_scaler = StandardScaler()

            num_cols = ['age','quantiy','price_per_unit','cogs']
            cat_cols = ['is_male','category']
            
            num_process = Pipeline([('impute',num_imputer),
                                    ('num_scaling',num_scaler)])
            
            cat_process = Pipeline([('onehot', OneHotEncoder(drop='first', handle_unknown='ignore'))
                                    ])

            processor = ColumnTransformer([('num_pipeline',num_process,num_cols),
                                           
                                           ('cat pipeline',cat_process,cat_cols)],
                                           remainder='passthrough')
    
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

            train_data = train_data.dropna(subset=[TARGET_COLUMN])
            test_data = test_data.dropna(subset=[TARGET_COLUMN])

            ## Did the mapping of Gender as Male -> 1; Female -> 0.
            input_feature_train_df = train_data.drop(columns=[TARGET_COLUMN])
            input_target_train_df = train_data[TARGET_COLUMN]

            input_feature_test_df = test_data.drop(columns=[TARGET_COLUMN])
            input_target_test_df = test_data[TARGET_COLUMN]

            # Get preprocessor and fit
            preprocessor = self.get_data_transformer()
            preprocessor_obj = preprocessor.fit(input_feature_train_df)

            # Transform features only
            transformed_train_features = preprocessor_obj.transform(input_feature_train_df)
            transformed_test_features = preprocessor_obj.transform(input_feature_test_df)

            # Combine transformed features with target
            train_arr = np.c_[transformed_train_features, input_target_train_df.to_numpy()]
            test_arr = np.c_[transformed_test_features, input_target_test_df.to_numpy()]

            logging.info("Transformed numerical data converted back to DataFrame.")

            ##Performing the categorical transformation
            logging.info(f"Performing One-Hot Encoding on columns: {CATEGORICAL_COL_TO_OHE}")
            
            ##Splitted the train-test data column speperately.

            # logging.info(f'test train feature == {input_feature_train_df.columns}')
            # logging.info(f'test test feature == {input_feature_test_df.columns}')

            logging.info(f"Final NumPy arrays created: Train shape {train_arr.shape}, Test shape {test_arr.shape}")

            save_numpy_obj(object_to_save=train_arr, file_path=self.data_transformation_config.transformed_train_file_path)
            save_numpy_obj(object_to_save=test_arr, file_path=self.data_transformation_config.transformed_test_file_path)
            save_obj(obj_to_save=preprocessor, file_path=self.data_transformation_config.trained_obj_file_path)

            save_obj(file_path="final_obj/preprocessor.pkl",obj_to_save=preprocessor)
            
            data_tranformation_artifact = DataTransformationArtifact(transformed_obj_file_path=self.data_transformation_config.trained_obj_file_path,
                                                                    train_obj_file_path=self.data_transformation_config.transformed_train_file_path,
                                                                    test_obj_file_path=self.data_transformation_config.transformed_test_file_path)
            logging.info("All transformed data and objects saved successfully.")
            
            return data_tranformation_artifact
        
        except Exception as e:
            raise CustomException(e,sys)