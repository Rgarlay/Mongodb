



''' Common constants defined for training pipeline '''

ARTIFACT_DIRECTORY: str = 'Archive'         ##Name of folder where everything is saved
TRAIN_FILE_NAME: str = 'train.csv'
TEST_FILE_NAME: str = 'test.csv'
FILE_NAME: str = 'Retail Sales Analysis.csv'
TARGET_COLUMN: str = 'total_sale'
PIPELINE_NAME: str = 'Retail Sales'


'''
Some constant of Data Ingestion. They start with DATA_INGESTION
'''
DATA_INGESTION_DATABASE_NAME: str = 'Session 3'
DATA_INGESTION_COLLECTION_NAME: str = 'CSV_Files'
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO: float = 0.75
DATA_INGESTION_DIR_NAME:str = 'data_ingestion'                 # THIS WILL HOARD THE 2 FOLDERS NAMED BELOW
DATA_INGESTION_FEATURE_STORE: str = 'feature_store'            #FILE PULLED FROM MONGODB
DATA_INGESTION_DATA_INGESTED: str = 'ingested'                 # TRAIN/TEST FILES WILL BE HERE


