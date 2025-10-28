from Retail.exception.exception import CustomException
from Retail.logging.logger import logging

import os,sys

import pymongo
import pandas as pd
import numpy as np

from dotenv import load_dotenv
load_dotenv()

mongo_db_url = os.getenv("uri")
client = pymongo.MongoClient(mongo_db_url)

from uvicorn import run as app_run
from Retail.pipelines.training_pipeline import TrainingPipeline
from Retail.utils.main_utils.utils import import_obj
from Retail.utils.ml_utils.model.estimator import RetailModel

import uvicorn 
from fastapi import FastAPI,File, UploadFile,Request


from fastapi.templating import Jinja2Templates
templates = Jinja2Templates(directory="./templates")


app = FastAPI()

@app.get("/")
def index():
    return f'This is the first page'

@app.get("/train")
async def train_route():
    try:
        training_pipeline = TrainingPipeline()
        training_pipeline.run_pipeline()
        return f"Tranining has finished"
    except Exception as e:
        raise CustomException(e,sys)
    
@app.post("/predict")
def predict_route(request: Request,file: UploadFile = File(...)):
    try:
        df=pd.read_csv(file.file)
        preprocesor=import_obj("final_obj/preprocessor.pkl")
        final_model=import_obj("final_obj/model.pkl")
        network_model = RetailModel(processor=preprocesor,model=final_model)
        y_pred = network_model.predict(df)
        df['predicted_column'] = y_pred
        print(df['predicted_column'])
        df.to_csv('valid_data/output.csv')
        return {'Messege':'Model validation has finished'}
    except Exception as e:
        raise CustomException(e,sys)

if __name__ == "__main__":
    app_run(app, host = '0.0.0.0', port = 8000)

    
