from Retail.exception.exception import CustomException
from Retail.logging.logger import logging

import os,sys

class RetailModel:
    def __init__(self,processor, model):
        try:
            self.model = model
            self.processor = processor
        except Exception as e:
            raise CustomException(e,sys)
    
    def predict(self,x):

        try:
            X_transform = self.processor.transform(x)
            y_hat = self.model.predict(X_transform)
            return y_hat
        except Exception as e:
            raise CustomException(e,sys)


    
