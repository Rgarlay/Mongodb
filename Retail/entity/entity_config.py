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

        