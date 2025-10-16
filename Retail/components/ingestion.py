from Retail.exception.exception import CustomException
from Retail.logging.logger import logging
from Retail.entity.entity_config import DataIngestionConfig
from Retail.entity.config_artifact import DataIngestionArtifact

import pandas as pd
import numpy as np
import json
import sys, os
from dotenv import load_dotenv

import pymongo
from sklearn.model_selection import train_test_split

load_dotenv()
MONGO_DB_URL = os.getenv("uri")

class DataIngestion:
    def __init__ (self, data_ingestion_config: DataIngestionConfig):
        try:
            self.data_ingestion_config = data_ingestion_config
            logging.info("DataIngestion initialized with provided DataIngestionConfig.")

        except Exception as e:
            raise CustomException(e,sys)
        
    def import_and_convert(self):
        '''
        Importing data from Mongodb and putting it into a 
        dataframe and returning that.
        '''
        try:
            logging.info('The importing process has started')
            
            mongo_client = pymongo.MongoClient(MONGO_DB_URL,serverSelectionTimeoutMS=60000, 
                                                        connectTimeoutMS=60000,
                                                        socketTimeoutMS=600000)

            logging.info("MongoDB connection established successfully.")
            database_name = self.data_ingestion_config.database_name
            logging.info(f'The name of the database is {database_name}')

            collection_name = self.data_ingestion_config.collection_name
            logging.info(f'The name of the collection is {collection_name}')
            
            collection = mongo_client[database_name][collection_name]
            logging.info(f'The number of record in collections is {len(list(collection.find()))}')

            dataframe = pd.DataFrame(list(collection.find()))
            cols_to_drop = ['transactions_id','customer_id', 'sale_date','sale_time']

            dataframe.drop(columns = cols_to_drop, inplace=True)

            if 'gender' in dataframe.columns:
                dataframe.rename(columns = {'gender':'is_male'}, inplace = True)
            
            if '_id' in dataframe.columns:
                dataframe.drop(columns = ['_id'],inplace=True)
#                logging.info({type(dataframe)})
            
            return dataframe
        except Exception as e:
            raise CustomException(e,sys)


    def data_export_to_feature_store(self,dataframe:pd.DataFrame):
        try:
            logging.info("Exporting data to feature store initiated.")
            feature_store_dir_name = self.data_ingestion_config.feature_store_name
            dir_path = os.path.dirname(feature_store_dir_name)
            os.makedirs(dir_path,exist_ok=True)
            dataframe.to_csv(feature_store_dir_name,index=False,header=True)
            
            return dataframe      
        except Exception as e:
            raise CustomException(e,sys)

    def df_train_test_split(self,dataframe:pd.DataFrame):
        try:
            logging.info(f'The train-test split has begun.')
            train_data, test_data = train_test_split(dataframe, train_size = self.data_ingestion_config.train_test_split_ratio)
            
            dir_name = os.path.dirname(self.data_ingestion_config.train_file_path)
            os.makedirs(dir_name,exist_ok=True)

            train_data.to_csv(self.data_ingestion_config.train_file_path,header=True, index=False)
            logging.info(f'The Train data has been saved. Length of dataframe: - {len(train_data)}')

            test_data.to_csv(self.data_ingestion_config.test_file_path,header=True, index=False)
            logging.info(f'The Test data has been saved. Length of dataframe: - {len(test_data)}')

            return train_data,test_data
        except Exception as e:
            raise CustomException(e,sys)
    
    def initiate_data_ingestion(self):
        try:
            logging.info("Data ingestion process initiated.")

            dataframe_1 = self.import_and_convert()
            dataframe_2 = self.data_export_to_feature_store(dataframe_1)
            self.df_train_test_split(dataframe_2)

            self.df_train_test_split(dataframe_2)
            logging.info("DataIngestionArtifact created and returned successfully.")

            data_ingestion_output = DataIngestionArtifact(train_file_path = self.data_ingestion_config.train_file_path,
                                                          test_file_path = self.data_ingestion_config.test_file_path)
            
            return data_ingestion_output
        except Exception as e:
            raise CustomException(e,sys)
        










