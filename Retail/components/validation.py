from Retail.exception.exception import CustomException
from Retail.logging.logger import logging
import os
import sys

from Retail.entity.artifact_config import DataIngestionArtifact,DatavalidationArtifact     #from dataclass code
from Retail.entity.entity_config import DataValidationConfig
from Retail.utils.main_utils.utils import read_yaml_file, write_ymal_file
import pandas as pd
from scipy.stats import ks_2samp

from Retail.constant.training_pipeline import SCHEMA_FILE_PATH


class DataValidation:
    def __init__(self, data_ingestion_artifact:DataIngestionArtifact,
                 data_validation_config: DataValidationConfig):
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config = data_validation_config
            self.schema_config = read_yaml_file(SCHEMA_FILE_PATH)           ##Path ffor the yaml file, that has the schema of columns
        except Exception as e:
            raise CustomException(e,sys)
        
    @staticmethod
    def read_data(file_path)->pd.DataFrame:
        '''
        Takes our data file and returns a pandas dataframe. 
        '''
        try:
            return pd.DataFrame(file_path)
        except Exception as e:
            raise CustomException(e,sys)
        
    def validate_number_of_columns(self,dataframe:pd.DataFrame) -> bool:
        '''
        Validates the Number of columns. Tells us whether the number of features in
        current file and base dataframe are the same. 
        '''
        try:
            number_of_columns = len(self.schema_config)
            logging.info(f'Required number of columns: {number_of_columns}')
            logging.info(f'DataFrame has columns: {len(dataframe.columns)}')
#            num_cols_base = dataframe.select_dtypes(include='number').columns.to_list()

            if len(dataframe.columns) == number_of_columns:# and data:
                return True
            return False
        except Exception as e:
            raise CustomException(e,sys)    
    
    def detect_dataset_drift(self,base_df, current_df, threshold = 0.05)->bool:

        '''Helps us determine 2 things.
        1. Whether there is any data drift (change of data distribution for any feature) and stores that is status variable.
        2. Generates and updates report if there is a data drift and write that into a file and saves it. 
        '''
        try:
            status = True
            report = {}
            for column in base_df:
                d1 = base_df[column]
                d2 = current_df[column]
                is_same_dist = ks_2samp(d1,d2)
                if threshold<=is_same_dist.pvalue:
                    is_found=False
                else:
                    is_found=True
                    status=False
            ##This thing is only changing when some data drift is there.
            report.update({column:{
                "p_value":float(is_same_dist.pvalue),
                "drift_status":is_found
            }})
            ##now we need report file path to put it there
            drift_report_file_path = self.data_validation_config.drift_report_file_path
            write_ymal_file(drift_report_file_path,content=report)
        except Exception as e:
            raise CustomException(e,sys)



    def initiate_data_validation(self)-> DataIngestionArtifact:
        '''
        Runs the entire code.
        '''
        try:
            train_file_path = self.data_ingestion_artifact.train_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path

            train_dataframe = self.read_data(train_file_path)
            test_dataframe = self.read_data(test_file_path)

            ## Validate number of columns for both train and test
            status = self.validate_number_of_columns(dataframe=train_dataframe)
            if not status:
                error_message = f'Train datadrame foes not contrain all the columns. \n'
                
            status = self.validate_number_of_columns(dataframe=test_dataframe)
            if not status:
                error_message = f'Test datadrame foes not contrain all the columns. \n'

            ## let's check datadraft in test file, referencing train_data file and saves it.

            status = self.detect_dataset_drift(base_df=train_dataframe,current_df=test_dataframe)
            dir_path = os.path.dirname(self.data_validation_config.valid_train_file_path)
            os.mkdirs(dir_path,exist_ok=True)

            ## Save our files 
            train_dataframe.to_csv(self.data_validation_config.valid_train_file_path,header=True,index=False)
            test_dataframe.to_csv(self.data_validation_config.valid_test_file_path,header=True,index=False)

            ## stores all the relevant information w.r.t this pipeline
            data_validation_artifact = DatavalidationArtifact(
                validation_status=status,
                valid_train_file_path=self.data_ingestion_artifact.train_file_path,
                valid_test_file_path=self.data_ingestion_artifact.test_file_path,
                invalid_train_file_path=None,
                invalid_test_file_path=None,
                drift_report_file_path=self.data_validation_config.drift_report_file_path
            )           

            return  data_validation_artifact

        except Exception as e:
            raise CustomException(e,sys)        

