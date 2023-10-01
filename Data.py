import requests
import io
import os
from bs4 import BeautifulSoup
import pandas as pd
from tabulate import tabulate
import opendatasets as od
import kaggle

os.environ['KAGGLE_USERNAME'] = "crissomar1"
os.environ['KAGGLE_KEY'] = "caf9604aa279620109b1cba4cca07226"
def get_data():
    #response = requests.get('https://www.kaggle.com/datasets/nguyenhoc/plane-crash/download?datasetVersionNumber=1')
    api = kaggle.KaggleApi()
    api.authenticate()
    #soup = BeautifulSoup(response.content, 'html.parser')
    #data = pd.read_csv(io.StringIO(soup.decode('utf-8')))
    return pd.read_csv('data.csv')

def print_data(df: pd.DataFrame):
    print(tabulate(df, headers=df.columns, tablefmt='orgtbl'))

def save_data(df: pd.DataFrame):
    df.to_csv('data.csv')

def main():
    data = get_data()
    print_data(data)
    save_data(data)