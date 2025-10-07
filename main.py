from Retail.components.ingestion import DataIngestion
from Retail.exception.exception import CustomException
from Retail.logging.logger import logging
from Retail.entity.entity_config import DataIngestionConfig,DataValidationConfig
from Retail.entity.entity_config import TrainingPipelineConfig
from Retail.components.validation import DataValidation
from Retail.utils.main_utils.utils import read_yaml_file,write_ymal_file


import sys
import os

if __name__ == "__main__":
    try:
        trainingpipelingconfig = TrainingPipelineConfig()
        dataingestionconfig = DataIngestionConfig(trainingpipelingconfig)
        dataingestion = DataIngestion(dataingestionconfig)
        logging.info('The code execution has begun')
        dataingestionartifact = dataingestion.initiate_data_ingestion()
        logging.info('Data Ingestion is complete')
        print(dataingestionartifact)

        data_validation_congfig = DataValidationConfig(trainingpipelingconfig)
        data_validation = DataValidation(dataingestionconfig,data_validation_congfig)
        logging.info("Initiate the data validation")
        data_validation_artifact = data_validation.initiate_data_validation()
        print(data_validation_artifact)

    except Exception as e:
        raise CustomException(e,sys)
    





    