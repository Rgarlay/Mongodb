import os,sys
from Retail.exception.exception import CustomException
from Retail.logging.logger import logging

from Retail.entity.entity_config import (
    training_pipeline,
    DataIngestionConfig,
    DataTransformationConfig,
    DataValidationConfig,
    ModelTrainerConfig,
    TrainingConfig
    )
from Retail.entity.config_artifact import (ModelTrainerArtifact,
                                           DataIngestionArtifact,
                                           DataTransformationArtifact,
                                           DataValidationArtifact)

from Retail.components.ingestion import DataIngestion,DataIngestionArtifact
from Retail.components.validation import DataValidation,DataValidationArtifact
from Retail.components.transformation import DataTransformation, DataValidationArtifact
from Retail.components.trainer import ModelTrainer,ModelTrainerArtifact


class TrainingPipeline:
    def __init__ (self):
        try:
            self.training_pipeline_config: str = TrainingConfig()
        except Exception as e:
            raise CustomException(e,sys)
    
    def initiate_data_ingestion(self):
        try:
            self.data_ingestion_config  = DataIngestionConfig(train_pipeline_config=self.training_pipeline_config)
            data_ingestion = DataIngestion(self.data_ingestion_config)
            data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
            
            return data_ingestion_artifact
        except Exception as e:
            raise CustomException(e,sys)
        
    def initiate_data_validation(self,data_ingestion_artifact: DataIngestionArtifact):
        try:
            self.data_validation_config = DataValidationConfig(self.training_pipeline_config)
            data_validation = DataValidation(data_ingestion_artifact=data_ingestion_artifact,
                                            data_validation_config=self.data_validation_config)
            
            data_validation_artifact = data_validation.initiate_data_validation()

            return data_validation_artifact
        except Exception as e:
            raise CustomException(e,sys)

    def initiate_data_transformation(self, data_validation_artifact: DataValidationArtifact):
        try:
            self.data_transformation_config = DataTransformationConfig(self.training_pipeline_config)
            data_transformation = DataTransformation(data_validation_artifact=data_validation_artifact,
                                                     data_transformation_config=self.data_transformation_config)
            
            data_transformation_artifact = data_transformation.initiate_data_transformation()

            return data_transformation_artifact
        except Exception as e:
            raise CustomException(e,sys)
        
    def initiate_model_training(self, data_transformation_artifact: DataTransformationArtifact):
        try:
            self.model_training_artifact: str = ModelTrainerConfig(self.training_pipeline_config)

            model_training = ModelTrainer(data_transformation_artifact=data_transformation_artifact,
                                          model_trainer_config=self.model_training_artifact)
            
            model_training_artifact = model_training.initiate_model_training()

            return model_training_artifact
        except Exception as e:
            raise CustomException(e,sys)

    def run_pipeline(self):
        try:
            data_ingestion_artifact = self.initiate_data_ingestion()
            data_validation_artifact = self.initiate_data_validation(data_ingestion_artifact=data_ingestion_artifact)
            data_transformation_artifact = self.initiate_data_transformation(data_validation_artifact=data_validation_artifact)
            model_trainer_artifact = self.initiate_model_training(data_transformation_artifact=data_transformation_artifact)

            return model_trainer_artifact
        except Exception as e:
            raise CustomException(e,sys)
