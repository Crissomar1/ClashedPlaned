import requests
import io
from bs4 import BeautifulSoup
import pandas as pd
from tabulate import tabulate


def get_data():
    response = requests.get('https://www.kaggle.com/datasets/nguyenhoc/plane-crash/download?datasetVersionNumber=1')
    soup = BeautifulSoup(response.content, 'html.parser')
    data = pd.read_csv(io.StringIO(soup.decode('utf-8')))
    return data

def print_data(df: pd.DataFrame):
    print(tabulate(df, headers=df.columns, tablefmt='orgtbl'))

def save_data(df: pd.DataFrame):
    df.to_csv('data.csv')

def main():
    data = get_data()
    print_data(data)
    save_data(data)