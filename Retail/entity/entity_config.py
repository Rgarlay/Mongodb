import os, sys
from Retail.exception.exception import CustomException
from Retail.logging.logger import logging
from Retail.constants import training_pipeline
from datetime import datetime

class TrainingConfig:
    def __init__ (self,timestamp = datetime.now()):
        timestamp = timestamp.strftime(format='%m_%d_%y_%M_%S')
        self.pipeline_name = training_pipeline.PIPELINE_NAME
        self.artifact_name = training_pipeline.ARTIFACT_DIRECTORY
        self.artifact_dir = os.path.join(self.artifact_name,timestamp)
        self.timestamp: str = timestamp

class DataIngestionConfig:
    def __init__(self, train_pipeline_config:TrainingConfig):

        self.data_ingestion_dir = os.path.join(train_pipeline_config.artifact_dir, training_pipeline.DATA_INGESTION_DIR_NAME)

        self.feature_store_name = os.path.join(self.data_ingestion_dir, 
                                               training_pipeline.DATA_INGESTION_FEATURE_STORE,
                                               training_pipeline.FILE_NAME)
        
        self.train_file_path = os.path.join(self.data_ingestion_dir,
                                             training_pipeline.DATA_INGESTION_DATA_INGESTED,
                                             training_pipeline.TRAIN_FILE_NAME)
        
        self.test_file_path = os.path.join(self.data_ingestion_dir,
                                             training_pipeline.DATA_INGESTION_DATA_INGESTED,
                                             training_pipeline.TEST_FILE_NAME)
        
        self.collection_name = training_pipeline.DATA_INGESTION_COLLECTION_NAME
        self.database_name = training_pipeline.DATA_INGESTION_DATABASE_NAME
        self.train_test_split_ratio = training_pipeline.DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO
        
        
        