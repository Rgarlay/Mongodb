from Retail.exception.exception import CustomException
from Retail.logging.logger import logging

## Call the config. file from the ingestion config.
from Retail.entity.entity_config import DataIngestionConfig

import os
import sys
from dotenv import load_dotenv
from typing import List
from sklearn.model_selection import train_test_split
import pymongo
from ..entity.artifact_config import DataIngestionArtifact
import pandas as pd
import numpy as np

load_dotenv()
MONGO_DB_URL = os.getenv("uri")

class DataIngestion:
    def __init__(self, data_ingestion_config:DataIngestionConfig):
        '''
        We are taking all the info and addresses from ingestion_config file.
        '''
        try:
            self.data_ingestion_config = data_ingestion_config  
        except Exception as e:
            raise CustomException(e,sys)
        
    ## we need to have dataframe from our mongo

    def export_collection_as_dataframe(self):
        '''
        Read data from Mongodb
        '''
        try:
            database_name = self.data_ingestion_config.database_name
            logging.info(f'Name of database {database_name}')
            collection_name = self.data_ingestion_config.collection_name
            logging.info(f'Name of collection {collection_name}')
            mongo_client = pymongo.MongoClient(MONGO_DB_URL, serverSelectionTimeoutMS=60000, 
                                                        connectTimeoutMS=60000,
                                                        socketTimeoutMS=600000)
            
            collection = mongo_client[database_name][collection_name]
            logging.info(f'The number of record in collections is {len(list(collection.find()))}')
            
            df = pd.DataFrame(list(collection.find()))
            #df.replace({'na':np.nan},inplace=True)
            logging.info(f'The type of df is {(df.shape)}')
            return df

        except Exception as e:
            raise CustomException(e,sys)         

    def export_data_into_feature_store(self,dataframe: pd.DataFrame):
        '''
        Saving our raw data, feature file into the directory.
        '''
        try:
            feature_store_file_path = self.data_ingestion_config.feature_store_file_path
            dir_path = os.path.dirname(feature_store_file_path)
            os.makedirs(dir_path,exist_ok=True)
            dataframe.to_csv(feature_store_file_path,index=False,header=True)
            return dataframe
        
        except Exception as e:
            raise CustomException(e,sys)

    def split_data_as_train_test(self, dataframe:pd.DataFrame):

        try:
            logging.info(f'{dataframe.shape}')
            train_set,test_set = train_test_split(dataframe,train_size=
                self.data_ingestion_config.train_test_split_ratio)
            logging.info('We have split our data into training and testing part successfully')

            logging.info('Exited split_data_as_train_test method of data ingestion class')

            dir_path = os.path.dirname(self.data_ingestion_config.training_fie_path)

            os.makedirs(dir_path,exist_ok=True)

            logging.info('Created dir for training and testing files')

            train_set.to_csv(
                self.data_ingestion_config.training_fie_path,index=False,header=True
                )
            test_set.to_csv(
                self.data_ingestion_config.testing_fie_path,index=False,header=True
            )

            logging.info('Exported training and testing file path successfully.')

        except Exception as e:
            raise CustomException(e,sys)


    def initiate_data_ingestion(self):
        try: 
            dataframe = self.export_collection_as_dataframe()
            dataframe = self.export_data_into_feature_store(dataframe) #saving dataframe
            self.split_data_as_train_test(dataframe)

            dataingestionartifact = DataIngestionArtifact(train_file_path=self.data_ingestion_config.training_fie_path,
                                                          test_file_path = self.data_ingestion_config.testing_fie_path)
        except Exception as e:
            raise CustomException(e,sys)