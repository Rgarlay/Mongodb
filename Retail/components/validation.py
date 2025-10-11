from Retail.exception.exception import CustomException
from Retail.logging.logger import logging

import pandas as pd
import numpy as np
from scipy.stats import ks_2samp

from dotenv import load_dotenv
load_dotenv()

import os,sys
from Retail.entity.entity_config import DataValidationConfig
from Retail.constants.training_pipeline import SCHEMA_FILE_PATH
from Retail.entity.config_artifact import DataIngestionArtifact,DataValidationArtifact
from Retail.utils.main_utils.utils import load_yaml_file,write_yaml_report


class DataValidation:
    def __init__(self,data_ingestion_artifact:DataIngestionArtifact,
                 data_validation_config: DataValidationConfig):    
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config = data_validation_config
            self.schema_file = load_yaml_file(SCHEMA_FILE_PATH)
            logging.info("Schema file successfully loaded from SCHEMA_FILE_PATH.")

        except Exception as e:
            raise CustomException(e,sys)
        
    
    @staticmethod
    def read_pd_file(file_path):
        try:
            dataframe = pd.read_csv(file_path)
            logging.info(f"Reading CSV file from path: {file_path}")
            return dataframe
        except Exception as e:
            raise CustomException(e,sys)
        
    def validate_no_of_cols(self,dataframe:pd.DataFrame):
        try:
            no_of_columns = len(self.schema_file)
            logging.info(f"Validating number of columns: Expected {len(self.schema_file)}, Found {len(dataframe.columns)}")
            no_of_df_cols = dataframe.columns
            if no_of_columns == len(no_of_df_cols):
                return True
            return False
        except Exception as e:
            raise CustomException(e,sys)
        
    def detect_dataset_drift(self,base_dataset,current_dataset, threshold):
        try:
            logging.info("Starting dataset drift detection using KS test.")
            status = True       ##Both distributions are the same
            report = {}
            for i in base_dataset.columns:
                d1 = base_dataset[i]
                d2 = current_dataset[i]
                is_same_dist = ks_2samp(d1,d2)
                if threshold <= is_same_dist.pvalue:        ##Threshold rejects our similarity
                    is_drift_found = False
                else:
                    is_drift_found=True
                    status=False
                report.update({i:
                                   {'pvalue': is_same_dist.pvalue,
                                    'is_drift': is_drift_found}})
            logging.info(f"Drift detection completed. Saving drift report at: {self.data_validation_config.drift_data_file_path}")
            drift_report_file_path = self.data_validation_config.drift_data_file_path

            dir_path = os.path.dirname(drift_report_file_path)
            os.makedirs(dir_path,exist_ok=True)

            write_yaml_report(content=report, file_path = self.data_validation_config.drift_data_file_path)
            logging.info("Drift report successfully written to YAML file.")
        except Exception as e:
            raise CustomException(e,sys)
        
    def initiate_data_validation(self):
        try:

            logging.info("Data validation process initiated.")
            train_file_path = self.data_ingestion_artifact.train_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path

            train_data = self.read_pd_file(train_file_path)
            test_data = self.read_pd_file(test_file_path)

            is_train_cols_same = self.validate_no_of_cols(train_data)
            is_test_cols_same = self.validate_no_of_cols(test_data)

            logging.info(f'The train data columns are {is_train_cols_same} and test data columns are {is_test_cols_same}')

            status = self.detect_dataset_drift(base_dataset=train_data,current_dataset=test_data,threshold=0.10)

            logging.info(f'The data drift report has bee properly kept')

            dir_name = os.path.dirname(self.data_validation_config.valid_train_file_path)

            os.makedirs(dir_name,exist_ok=True)

            train_data.to_csv(self.data_validation_config.valid_train_file_path,header=True,index=False)
            test_data.to_csv(self.data_validation_config.valid_test_file_path,header=True,index=False)

            logging.info("Validated datasets saved successfully.")
            logging.info("DataValidationArtifact created successfully and ready for return.")

            data_validation_artifact = DataValidationArtifact(
                validation_status= status,
                valid_train_file_path = train_file_path,
                valid_test_file_path = test_file_path,
                invalid_train_file_path = None,
                invalid_test_file_path = None,
                drift_report_file_path = self.data_validation_config.drift_data_file_path
            )

            return data_validation_artifact
        except Exception as e:
            raise CustomException(e,sys)
        

    

        

