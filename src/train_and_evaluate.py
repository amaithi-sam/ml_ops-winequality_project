# Load the Train and test Files

# Train the Algo

# Save the Metrics & Parameters

import os
import pandas
import warnings
import sys
import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.linear_model import ElasticNet

from get_data import read_params
import argparse
import joblib
import json

import mlflow 
from urllib.parse import urlparse


def eval_metrics(y_true, y_pred):
    rmse = mean_squared_error(y_true, y_pred)
    mae = mean_absolute_error(y_true, y_pred)
    r2 = r2_score(y_true, y_pred)

    return rmse, mae, r2


def train_and_evaluate(config_path):
    config = read_params(config_path)
    test_data_path = config["split_data"]["test_path"]
    train_data_path = config["split_data"]["train_path"]
    random_state = config["base"]["random_state"]
    model_dir = config["model_dir"]

    alpha = config["estimator"]["ElasticNet"]["params"]["alpha"]
    l1_ratio = config["estimator"]["ElasticNet"]["params"]["l1_ratio"]
    target = [config["base"]["target_col"]]

    train = pd.read_csv(train_data_path, sep=',', encoding="utf-8")
    test = pd.read_csv(test_data_path, sep=',', encoding="utf-8")

    train_y = train[target]
    test_y = test[target]

    train_x = train.drop(target, axis=1)
    test_x = test.drop(target, axis=1)

#----------------ML FLOW-------------------
    ml_flow_config = config["ml_flow_config"]
    remote_server_uri = ml_flow_config["remote_server_uri"]

    mlflow.set_tracking_uri(remote_server_uri)

    mlflow.set_experiment(ml_flow_config["experiment_name"])

    with mlflow.start_run(run_name=ml_flow_config["run_name"]) as mlops_run:

        lr = ElasticNet(
            alpha=alpha,
            l1_ratio=l1_ratio,
            random_state=random_state
        )

        lr.fit(train_x, train_y)

        predicted_qualities = lr.predict(test_x)

        (rmse, mae, r2) = eval_metrics(test_y, predicted_qualities)


    # -------------------------------------------------
        mlflow.log_param("alpha", alpha)
        mlflow.log_param("l1_ratio", l1_ratio)
        mlflow.log_metric("rmse", rmse)
        mlflow.log_metric("mae", mae)
        mlflow.log_metric("r2", r2)

        tracking_url_type_store = urlparse(mlflow.get_artifact_uri()).scheme

        if tracking_url_type_store != "file":
            mlflow.sklearn.log_model(lr, "model", registered_model_name=ml_flow_config["registered_model_name"])

        else:
            mlflow.sklearn.load_model(lr, "model")

    # -------------------------------------------------


if __name__ == "__main__":
    args = argparse.ArgumentParser()
    args.add_argument("--config", default="params.yaml")
    parsed_args = args.parse_args()
    train_and_evaluate(parsed_args.config)
