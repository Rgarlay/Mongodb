import os
import sys
import pandas as pd
import numpy as np

'''
Defining common constants variable for training pipeline
'''

TARGET_COLUMN: str = "total_sale"               # From csv file
PIPELINE_NAME: str = "Retail Sales"             # Yet to figure out
ARTIFACT_DIR: str = "Archive"               #maybe the adress of file
FILE_NAME: str = "Retail Sales Analysis.csv"     

TRAIN_FILE_NAME: str = "train.csv"
TEST_FILE_NAME: str = "test.csv"


'''
Data ingestion related constants start wiwth DATA_INGESTION VAR NAME
'''

DATA_INGESTION_DATABASE_NAME: str = "CSV_FILE"
DATA_INGESTION_COLLECTION_NAME: str = "Session 2"        #THESE 2TAKEN FROM MONGO-DB
DATA_INGESTION_DIR_NAME: str = "data_ingestion"         
DATA_INGESTION_FEATURE_STORE: str = "feature_store"         #This is the entire file that is pulled from Mongodb.
DATA_INGESTION_INGESTED_DIR: str = "ingested"           #will make these later
DATA_INGESTION_TRAIN_TEST_SPLIT: float = 0.2        #Will need in splitting

