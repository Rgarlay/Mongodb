from Retail.exception.exception import CustomException
from Retail.logging.logger import logging

from Retail.entity.entity_config import (DataIngestionConfig,
                                         TrainingConfig,
                                         DataValidationConfig,
                                         DataTransformationConfig,
                                         ModelTrainerConfig)


from Retail.components.ingestion import DataIngestion
from Retail.components.validation import DataValidation
from Retail.components.transformation import DataTransformation
from Retail.components.trainer import ModelTrainer


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
        
        validation_config = data_validation.initiate_data_validation()

        logging.info(f'Data Transformation has begun.')
        data_transformation_config = DataTransformationConfig(training_config)
        data_transformation = DataTransformation(data_transformation_config=data_transformation_config,
                                                data_validation_artifact=validation_config)
        
        transformation_config = data_transformation.initiate_data_transformation()

        logging.info('Model Training has begun.')
        model_trainer_config = ModelTrainerConfig(training_config)
        model_trainer = ModelTrainer(model_trainer_config=model_trainer_config,
                                     data_transformation_artifact=transformation_config)
        
        trainer_config = model_trainer.initiate_model_training()

        print(trainer_config)

    except Exception as e:
        raise CustomException(e,sys)