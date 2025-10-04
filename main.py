from Retail.components.ingestion import DataIngestion
from Retail.exception.exception import CustomException
from Retail.logging.logger import logging
from Retail.entity.entity_config import DataIngestionConfig
from Retail.entity.entity_config import TrainingPipelineConfig

import sys
import os

if __name__ == "__main__":
    try:
        trainingpipelingconfig = TrainingPipelineConfig()
        dataingestionconfig = DataIngestionConfig(trainingpipelingconfig)
        dataingestion = DataIngestion(dataingestionconfig)
        logging.info('The code execution has begun')
        dataingestion.initiate_data_ingestion()
        print(dataingestion)
    except Exception as e:
        raise CustomException(e,sys)
    





    