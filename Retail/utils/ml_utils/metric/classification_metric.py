from Retail.exception.exception import CustomException
from Retail.logging.logger import logging
import os,sys
from Retail.entity.config_artifact import ClassificationMetricArtifact
import numpy as np
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error

def get_classification_score(y_test,y_pred):
    try:
        r2_score_value = r2_score(y_test,y_pred)
        root_mean_squared_error_value = np.sqrt(mean_squared_error(y_test,y_pred))
        mean_absolute_error_value = mean_absolute_error(y_test,y_pred)

        classification_artifact = ClassificationMetricArtifact(r2_score=r2_score_value,
                                                               root_mean_squared_error=root_mean_squared_error_value,
                                                               mean_absolute_error=mean_absolute_error_value)
        
        return classification_artifact
    except Exception as e:
        raise CustomException(e,sys)