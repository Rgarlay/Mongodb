from Retail.exception.exception import CustomException
from Retail.logging.logger import logging
from Retail.entity.entity_config import DataIngestionConfig
from Retail.entity.config_artifact import DataIngestionArtifact
from Retail.components.ingestion import DataIngestion
from Retail.entity.entity_config import DataIngestionConfig,TrainingConfig
import os, sys

if __name__ == "__main__":
    try:
        training_config = TrainingConfig()
        data_ingest_config = DataIngestionConfig(training_config)
        data_ingestion = DataIngestion(data_ingest_config)
        dataingestionartifact = data_ingestion.initiate_data_ingestion()
        logging.info('The data ingestion has begun.')

        print(dataingestionartifact)
    except Exception as e:
        raise CustomException(e,sys)