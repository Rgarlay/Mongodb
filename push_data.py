import pymongo
from dotenv import load_dotenv
import os
import json
import certifi


load_dotenv()

MONGO_URL = os.getenv("uri")
client = pymongo.MongoClient(MONGO_URL)

ca = certifi.where()

from Retail.exception.exception import CustomException
from Retail.logging.logger import logging
import pandas as pd
import numpy as np
import sys

class RetailDataExtract():
    def __init__ (self):
        try:
            pass
        except Exception as e:
            CustomException(e,sys)


    def csv_to_json(self, file_path):
        try:
            #import data
            df = pd.read_csv(file_path)
            #Removed indexes
            df = df.reset_index()
            # Transposed --> Converted to json --> took values --> put everything into the list to make it proper format. 
            records = list(json.loads(df.T.to_json()).values())
            return records
        
        except Exception as e:
            raise CustomException(e,sys)

    def upload_to_mongodb(self, database,collection,records):
        try:
            self.database = database
            self.collection = collection
            self.records = records

            self.mongo_client = pymongo.MongoClient(MONGO_URL)

            self.database = self.mongo_client[self.database]
            self.collection = self.database[self.collection]
            self.collection.insert_many(self.records)
            return len(self.records)
        except Exception as e:
            raise CustomException(e,sys)
        

if __name__ == "__main__":
    FILE_PATH = r"C:\Users\rgarlay\Desktop\DS\Mongo db\archive\SQL - Retail Sales Analysis_utf .csv"
    database = "CSV_FILE"
    collection = "Session 2"
    retail_obj = RetailDataExtract()
    records = retail_obj.csv_to_json(file_path=FILE_PATH)
    no_of_records = retail_obj.upload_to_mongodb(database=database,collection=collection,records=records)