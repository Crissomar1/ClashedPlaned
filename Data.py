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

def get_data2() -> pd.DataFrame:
    #read from file in "Data" folder
    df = pd.read_csv('Data/planecrashinfo_20181121001952.csv',index_col=0)
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
    
    df['time'] = df['time'].apply(lambda x: x.replace('"',':'))
    df['time'] = df['time'].apply(lambda x: x.replace(';',':'))
    df['time'] = df['time'].apply(lambda x: x.replace('.',':'))
    df['time'] = df['time'].apply(lambda x: x.replace(' ',''))
    
    #borra las "c","C","Z","z" de la columna time
    df['time'] = df['time'].apply(lambda x: x.strip('c'))
    df['time'] = df['time'].apply(lambda x: x.strip('C'))
    df['time'] = df['time'].apply(lambda x: x.strip('Z'))
    df['time'] = df['time'].apply(lambda x: x.strip('z'))
    df['time'] = df['time'].apply(lambda x: x.strip(':'))
    
    df['time'] = df['time'].apply(lambda x: x if len(x) > 2 else '?')
    #donde no hay : lo ponemos 2 caracteres antes del final
    df['time'] = df['time'].apply(lambda x: x if ':' in x else x[:-2] + ':' + x[-2:])
    df['time'] = df['time'].apply(lambda x: x if len(x) > 2 else '?')
    #reset index
    df = df.reset_index()
    #Dividimos la columna date en 3 columnas nuevas (day, month, year) formato: month day, year
    df[['month','day','year']] = df['date'].str.split(' ',expand=True)
    #borramos la columna date
    df = df.drop(['date'], axis=1)
    df["day"] = df["day"].apply(lambda x: x.strip(','))
    #en fatalities, aboard y ground donde hay ? lo cambiamos por 0
    df['fatalities'] = df['fatalities'].apply(lambda x: x if x != '?' else '0')
    df['aboard'] = df['aboard'].apply(lambda x: x if x != '?' else '0')
    df['ground'] = df['ground'].apply(lambda x: x if x != '?' else '0')
    #convertimos la columna year a int
    df['year'] = df['year'].astype(int)
    #convertimos la columna day a int
    df['day'] = df['day'].astype(int)
    #convertimos la columna fatalities a int
    df['fatalities'] = df['fatalities'].astype(int)
    #convertimos la columna aboard a int
    df['aboard'] = df['aboard'].astype(int)
    #convertimos la columna ground a int
    df['ground'] = df['ground'].astype(int)
    
    return df

def stats(df: pd.DataFrame):
    
    #total number of crashes
    print("Total number of crashes: ", len(df))
    #total number of fatalities (? in data doesnt count)
    print("Total number of fatalities: ", df['fatalities'].sum())
    #total number of fatalities per year
    print("Total number of fatalities per year: ")
    print(df.groupby(['year'])['fatalities'].sum())
    #total number of fatalities per month
    print("Total number of fatalities per month: ")
    print(df.groupby(['month'])['fatalities'].sum())
    #mean number of fatalities per year
    print("Mean number of fatalities per year: ")
    print(df.groupby(['year'])['fatalities'].mean())
    #year with most fatalities
    print("Year with most fatalities: ")
    print(df.groupby(['year'])['fatalities'].sum().idxmax())
    #year with least fatalities
    print("Year with least fatalities: ")
    print(df.groupby(['year'])['fatalities'].sum().idxmin())


def main():
    data = clean_data(get_data2())
    #stats(data)
    print_data(data)
    save_data(data)

main()