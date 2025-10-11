from Retail.exception.exception import CustomException
from Retail.logging.logger import logging

from Retail.entity.entity_config import DataIngestionConfig,DataValidationConfig
#from Retail.entity.config_artifact import DataIngestionArtifact,DataValidationArtifact

from Retail.components.ingestion import DataIngestion
from Retail.components.validation import DataValidation
from Retail.entity.entity_config import DataIngestionConfig,TrainingConfig,DataValidationConfig





import os, sys

if __name__ == "__main__":
    try:
        training_config = TrainingConfig()

        logging.info('The data ingestion has begun.')
        data_ingest_config = DataIngestionConfig(training_config)
        data_ingestion = DataIngestion(data_ingest_config)
        dataingestionartifact = data_ingestion.initiate_data_ingestion()
        
        logging.info('The data validation has begun.')
        data_validation_config = DataValidationConfig(training_config)
        data_validation = DataValidation(data_validation_config=data_validation_config,
                                         data_ingestion_artifact=dataingestionartifact)
        
        data_validation_config = data_validation.initiate_data_validation()

        print(data_ingest_config)
    except Exception as e:
        raise CustomException(e,sys)