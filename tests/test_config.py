import pytest 
import logging 
import os 
import joblib 
import json 
from prediction_service.prediction import api_response, form_response, NotInCols, NotInRange
import prediction_service


input_data = {
    "incorrect_range": {
        "fixed_acidity": 100,
        "volatile_acidity":85,
        "citric_acid":45,
        "residual_sugar":25,
        "chlorides":55,
        "free_sulfur_dioxide":80,
        "total_sulfur_dioxide":400,
        "density":5,
        "pH":8,
        "sulphates":55,
        "alcohol":35},
    
    "correct_range": {
        "fixed_acidity": 10,
        "volatile_acidity": 0.14,
        "citric_acid":0.5,
        "residual_sugar":10,
        "chlorides":0.5,
        "free_sulfur_dioxide":30,
        "total_sulfur_dioxide":100,
        "density":1.0,
        "pH":3,
        "sulphates":1.25,
        "alcohol":10},
    
    "incorrect_cols": {
        "fixed acidity": 10,
        "volatile acidity": 0.14,
        "citric acid":0.5,
        "residual sugar":10,
        "chlorides":0.5,
        "free sulfur dioxide":30,
        "total sulfur dioxide":100,
        "density":1.0,
        "pH":3,
        "sulphates":1.25,
        "alcohol":10}

}   

TARGET_range = {
    "min" : 3.0,
    "max" : 8.0
}

def test_form_response_correct_range(data=input_data["correct_range"]):
    res = form_response(data)
    assert TARGET_range["min"] <= res <= TARGET_range["max"]

def test_api_response_correct_range(data=input_data["correct_range"]):
    res = api_response(data)
    assert TARGET_range["min"] <= res["response"] <= TARGET_range["max"]
 
def test_form_response_incorrect_range(data=input_data["incorrect_range"]):
    with pytest.raises(prediction_service.prediction.NotInRange):
        res =form_response(data)

def test_api_response_incorrect_range(data=input_data["incorrect_range"]):
    res =api_response(data)
    assert res["response"] == prediction_service.prediction.NotInRange().message


def test_api_response_incorrect_column(data=input_data["incorrect_cols"]):
    res =api_response(data)
    assert res["response"] == prediction_service.prediction.NotInCols().message
