#READ THE DATA FROM DATA SOURCE 
# SAVE IT IN THE DATA/RAW FOR FURTHER PROCESS

import os 
from get_data import read_params, get_data 
import argparse 

def load_and_save(config_path):
    config = read_params(config_path)
    df = get_data(config_path)

