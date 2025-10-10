import pandas as pd
import numpy as np
from Retail.exception.exception import CustomException
from Retail.logging.logger import logging

import json
import pymongo
import os,sys
from dotenv import load_dotenv

load_dotenv()

MONGO_DB_CONNECT = os.getenv('uri')


class push_data:
    def __init__(self):
        try:
            pass
        except Exception as e:
            raise CustomException(e,sys)
        
    def csv_to_json(self,file_path):
        try:

            df = pd.read_csv(file_path)
            df = df.reset_index()
            print(df.head())
            json_files = list(json.loads(df.T.to_json()).values())
            return json_files
        except Exception as e:
            raise CustomException(e,sys)
    
    def uploading_to_mongodb(self,colleciton, database,records):
        
        try:
            self.collection = colleciton
            self.database = database
            self.records = records

            mongo_db = pymongo.MongoClient(MONGO_DB_CONNECT)

            colleciton_name = mongo_db[self.database][self.collection]

            colleciton_name.insert_many(self.records)

            print(len(self.records))

        except Exception as e:
            raise CustomException(e,sys)
        
if __name__ == "__main__":
    collection = 'Session_3'
    database = "CSV_FILE"
    new_insertion = push_data()
    file_path = r'archieve\Retail Sales Analysis.csv'
    record = new_insertion.csv_to_json(file_path=file_path)
    pushing_to_db = new_insertion.uploading_to_mongodb(collection,database,record)
