import numpy as np
import os,sys

SCHEMA_FILE_PATH: str = os.path.join('data_schema','schema.yaml')
PREPROCESSING_OBJECT_FILE_NAME = "preprocessing.pkl"

''' Common constants defined for training pipeline '''

TARGET_COLUMN: str = 'total_sale'
GENDER_COLUMN_TO_MAP: str = 'is_male'
CATEGORICAL_COL_TO_OHE: str = 'category'


ARTIFACT_DIRECTORY: str = 'archieve'         ##Name of folder where everything is saved
TRAIN_FILE_NAME: str = 'train.csv'
TEST_FILE_NAME: str = 'test.csv'
FILE_NAME: str = 'Retail Sales Analysis.csv'
PIPELINE_NAME: str = 'Retail Sales'

'''
Constant of Data Ingestion part in pipeline. They start with DATA_INGESTION
'''
DATA_INGESTION_COLLECTION_NAME: str = 'Session_3'
DATA_INGESTION_DATABASE_NAME: str = 'CSV_FILE'
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO: float = 0.75
DATA_INGESTION_DIR_NAME:str = 'data_ingestion'                 # THIS WILL HOARD THE 2 FOLDERS NAMED BELOW
DATA_INGESTION_FEATURE_STORE: str = 'feature_store'            #FILE PULLED FROM MONGODB
DATA_INGESTION_DATA_INGESTED: str = 'ingested'                 # TRAIN/TEST FILES WILL BE HERE


'''
Constants of Data Validation part in pipeline. They start with DATA_VALIDATION
'''
DATA_VALIDATION_DIR_NAME: str = 'data_validation'
DATA_VALIDATION_VALID_DIR: str = 'valid'
DATA_VALIDATION_INVALID_DIR: str = 'Invalid'
DATA_VALIDATION_DRIFT_REPORT_DIR: str = 'drift_report'
DATA_VALIDATION_DRIFT_REPORT_FILE_NAME: str = 'drift_report.yaml'

'''
Common constants of Data Transformation related constants start with DATA_TRANSFORMATION_ VAR NAME
'''
DATA_TRANSFORMATION_IMPUTE_PARAMS: dict = {
    "missing_values":np.nan,
    "n_neighbors":3,
    "weights":"uniform"
}
DATA_TRANSFORMATION_TRAIN_FILE_NAME: str = "train.npy"
DATA_TRANSFORMATION_TEST_FILE_NAME: str = "test.npy"

DATA_TRANSFORMATION_DIR_NAME: str = "data_transformation"
DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR: str = "transformed"
DATA_TRANSFORMATION_TRANSFORMED_OBJ_DIR: str = "transformed_object"