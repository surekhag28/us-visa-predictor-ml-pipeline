import os
import sys
import mlflow
import pandas as pd
import numpy as np

from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import (accuracy_score, 
                            precision_score, 
                            recall_score, 
                            f1_score,
                            classification_report)

from xgboost import XGBClassifier
from sklearn.model_selection import RandomizedSearchCV

from src.logger import logging as logger
from src.exception import *
from src.constants import (
                            SCHEMA_FILE_PATH, 
                            MLFLOW_TRACKING_URI,
                            MODEL_TRAINER_EXPECTED_SCORE,
                            METRICS_DIR
                           )
from src.utils import save_object
from src.utils import load_numpy_array
from src.config.config import (
                                    DataTransformationOutput,
                                    ModelTrainerInput,
                                    ClassificationMetric
                                )


class ModelTrainer:
    def __init__(self, data_transformation_output: DataTransformationOutput,
                 model_trainer_input: ModelTrainerInput):
        self.data_transformation_output = data_transformation_output
        self.model_trainer_input = model_trainer_input
        
    
    def train_model(self, train_arr, test_arr):
        
        hyperparameters = {
                            'xgboost_params' : {
                                'max_depth':range(3,10,2),
                                'min_child_weight':range(1,6,2)
                            },
                            'rf_params' : {
                                'max_depth': [10, 12, None, 15, 20],
                                'max_features': ['sqrt', 'log2', None],
                                'n_estimators': [10, 50, 100, 200]
                            },
                            'gradient_params' : {
                                'max_depth': [10, 12, None, 15, 20],
                                'n_estimators': [10, 50, 100, 200]
                            }
                        }
        
        models = [
                        ('XGBoost', XGBClassifier(), hyperparameters['xgboost_params']),
                        ('RF', RandomForestClassifier(), hyperparameters['rf_params']),
                        ('GradientBoost', GradientBoostingClassifier(), hyperparameters['gradient_params'])
                    ]
        
        X_train, y_train, X_test, y_test = (
                                                train_arr[:,:-1],
                                                train_arr[:,-1],
                                                test_arr[:,:-1],
                                                test_arr[:,-1]
                                            )  
        
        mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
        mlflow.set_experiment('US_Visa_Prediction_Experiment')
        
        best_accuracy = 0
        best_models = {}
        best_model_details = {}
        
        logger.info('Initiated the training process')
        
        try:
            #train models and find best hyperparameters using GridSearchCV
            for name, model, params in models:
                with mlflow.start_run(run_name=name):
                    logger.info('Training model : {}'.format(name))
                    grid_search = GridSearchCV(model, param_grid=params, scoring='accuracy', cv=5, n_jobs=-1)
                    grid_search.fit(X_train, y_train)
                    
                    
                    best_models[name] = grid_search.best_estimator_
                    logger.info('Best parameters for {}: {}'.format(name,grid_search.best_params_))
                    logger.info('Best score for {}: {}'.format(name, grid_search.best_score_))
                
                    # evaluation on test data 
                    y_pred = best_models[name].predict(X_test)
                    accuracy = accuracy_score(y_test, y_pred)
                    
                    logger.info("Test performance of model {} : {}".format(name, accuracy))
                    

                    mlflow.log_params(grid_search.best_params_)
                    mlflow.log_metric('accuracy',accuracy)
                    
                    logger.info('MLflow Run ID: {}'.format(mlflow.active_run().info.run_id))
                    
                    if((accuracy > MODEL_TRAINER_EXPECTED_SCORE) and (accuracy > best_accuracy)):
                        best_accuracy = accuracy
                        best_model_details = {
                            'name': name,
                            'model': grid_search.best_estimator_,
                            'params': grid_search.best_params_,
                            'accuracy': best_accuracy
                        }
            
            
            logger.info('Found the best model as {} with this configuration: {}'.format(best_model_details['name'], best_model_details['model']))
            logger.info('Training process completed')

            return best_model_details
        except Exception as e:
            raise USvisaException(e, sys)
          
    def evaluate_model(self, best_model_details, test_arr):
        
        logger.info('Started evaluating the best model on test data')
          
        try:
            save_object(self.model_trainer_input.trained_model_file_path, best_model_details['model'])
            logger.info('Saved best model in the directory')
            
            y_pred = best_model_details['model'].predict(test_arr[:,:-1])
            f1 = f1_score(test_arr[:,-1], y_pred)
            precision = precision_score(test_arr[:,-1], y_pred)
            recall = recall_score(test_arr[:,-1], y_pred)
            report = classification_report(test_arr[:,-1], y_pred)
            
            with open(f'{METRICS_DIR}/best_model_classification_report.txt','w') as f:
                f.write(report)
            
            metric_output = ClassificationMetric(f1_score=f1, precision_score=precision, recall_score=recall)
            
            with mlflow.start_run(run_name='Best Model') as run:
                mlflow.log_param('best_model_name', best_model_details['name'])
                mlflow.log_params(best_model_details['params'])
                mlflow.log_metric('best accuracy', best_model_details['accuracy'])
                mlflow.log_artifact(f'{METRICS_DIR}/best_model_classification_report.txt')
            
            logger.info('Finished model evaluation on test data')
            return metric_output
        except Exception as e:
            raise USvisaException(e, sys)
    
    def run_model_trainer(self):
        logger.info("Initiated the model training process")
        
        try:
            train_arr = load_numpy_array(self.data_transformation_output.processed_train_file_path)
            test_arr = load_numpy_array(self.data_transformation_output.processed_test_file_path)
            
            best_model_details = self.train_model(train_arr, test_arr)

            metrics = self.evaluate_model(best_model_details, test_arr)
            
            logger.info("Exit from the training process")
            
            logger.info("---------Model Performance Report----------")
            logger.info(metrics)
        except Exception as e:
            raise USvisaException(e, sys)