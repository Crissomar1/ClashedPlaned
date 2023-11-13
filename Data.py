import requests
import io
import os
from bs4 import BeautifulSoup
import pandas as pd
from tabulate import tabulate
import opendatasets as od




def get_data() -> pd.DataFrame:
    response = requests.get('https://raw.githubusercontent.com/Crissomar1/ClashedPlaned/Tarea-1/Data/planecrashinfo_20181121001952.csv')
    #its a raw html so we need to decode it
    data = response.content.decode('utf-8')
    #we need to convert it to a pandas dataframe
    df = pd.read_csv(io.StringIO(data),index_col=0)
    return df

def print_data(df: pd.DataFrame):
    print(tabulate(df, headers=df.columns, tablefmt='orgtbl'))

def save_data(df: pd.DataFrame):
    df.to_csv('data.csv')

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    #leave column 11 and 12 just with the first number
    df['aboard'] = df['aboard'].apply(lambda x: x.split(' ')[0])
    df['fatalities'] = df['fatalities'].apply(lambda x: x.split(' ')[0])
    df = df.drop(['flight_no'], axis=1)
    df = df.drop(['registration'], axis=1)
    df = df.drop(['summary'], axis=1)
    
    return df


def main():
    data = clean_data(get_data())
    print_data(data)
    save_data(data)

main()