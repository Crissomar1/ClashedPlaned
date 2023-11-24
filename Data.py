import requests
import io
import os
from bs4 import BeautifulSoup
import pandas as pd
from tabulate import tabulate
import opendatasets as od
import matplotlib.pyplot as plt
import statsmodels.api as sm
from statsmodels.formula.api import ols
from statsmodels.stats.anova import anova_lm



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
    #? por ""
    df['time'] = df['time'].apply(lambda x: x if x != '?' else '')
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

    ## Localidades

    #"?" por ""
    df['location'] = df['location'].apply(lambda x: x if x != '?' else '')
    #creamos una columna country y city
    #data$LOCATION<-gsub(".*,","",data$location)
    df[['city','country']] = df['location'].str.split(', ',n=1,expand=True)
    df = df.drop(['location'], axis=1)
    # fix misspelled country names
    df['country'] = df['country'].apply(lambda x: x if x != 'Afghanstan' else 'Afghanistan')
    df['country'] = df['country'].apply(lambda x: x if x != 'Alaksa' else 'Alaska')
    df['country'] = df['country'].apply(lambda x: x if x != 'Alakska' else 'Alaska')
    df['country'] = df['country'].apply(lambda x: x if x != 'AK' else 'Arkansas')
    df['country'] = df['country'].apply(lambda x: x if x != 'Azores (Portugal)' else 'Portugal')
    df['country'] = df['country'].apply(lambda x: x if x != 'Baangladesh' else 'Bangladesh')
    df['country'] = df['country'].apply(lambda x: x if x != 'Belgian Congo (Zaire)' else 'Belgian Congo')
    df['country'] = df['country'].apply(lambda x: x if x != 'Belgium Congo' else 'Belgian Congo')
    df['country'] = df['country'].apply(lambda x: x if x != 'Boliva' else 'Bolivia')
    df['country'] = df['country'].apply(lambda x: x if x != 'Bosnia-Herzegovina' else 'Bosnia Herzegovina')
    df['country'] = df['country'].apply(lambda x: x if x != 'British Columbia Canada' else 'British Columbia')
    df['country'] = df['country'].apply(lambda x: x if x != 'Bugaria' else 'Bulgaria')
    df['country'] = df['country'].apply(lambda x: x if x != 'bulgaria' else 'Bulgaria')
    df['country'] = df['country'].apply(lambda x: x if x != 'Burma (Myanmar)' else 'Myanmar')
    df['country'] = df['country'].apply(lambda x: x if x != 'CA' else 'California')
    df['country'] = df['country'].apply(lambda x: x if x != 'Cailifornia' else 'California')
    df['country'] = df['country'].apply(lambda x: x if x != 'Calilfornia' else '')
    df['country'] = df['country'].apply(lambda x: x if x != 'Cameroons' else 'Cameroon')
    df['country'] = df['country'].apply(lambda x: x if x != 'Canada2' else 'Canada')
    df['country'] = df['country'].apply(lambda x: x if x != 'Cape Verde Islands' else 'Cape Verde')
    df['country'] = df['country'].apply(lambda x: x if x != 'Coloado' else 'Colorado')
    df['country'] = df['country'].apply(lambda x: x if x != 'Columbia' else 'Colombia')
    df['country'] = df['country'].apply(lambda x: x if x != 'Comoro Islands' else 'Comoros')
    df['country'] = df['country'].apply(lambda x: x if x != 'Comoros Islands' else 'Comoros')
    df['country'] = df['country'].apply(lambda x: x if x != 'Congo Democratic Republic' else 'Democratic Republic of the Congo')
    df['country'] = df['country'].apply(lambda x: x if x != 'Congo' else 'Democratic Republic of the Congo')
    df['country'] = df['country'].apply(lambda x: x if x != 'D.C.' else 'Washington D.C.')
    df['country'] = df['country'].apply(lambda x: x if x != 'Deleware' else 'Delaware')
    df['country'] = df['country'].apply(lambda x: x if x != 'Democratic Republic Cogo' else 'Democratic Republic of the Congo')
    df['country'] = df['country'].apply(lambda x: x if x != 'Democratic Republic Congo' else 'Democratic Republic of the Congo')
    df['country'] = df['country'].apply(lambda x: x if x != 'Democratic Republic of Congo ' else 'Democratic Republic of the Congo')
    df['country'] = df['country'].apply(lambda x: x if x != 'Democratic Republic of the Congo' else 'Democratic Republic of the Congo')
    df['country'] = df['country'].apply(lambda x: x if x != 'Democtratic Republic Congo ' else '')
    df['country'] = df['country'].apply(lambda x: x if x != 'Djbouti' else 'Djibouti')
    df['country'] = df['country'].apply(lambda x: x if x != 'Domincan Republic' else 'Dominican Republic')
    df['country'] = df['country'].apply(lambda x: x if x != 'Dominica' else 'Dominican Republic')
    df['country'] = df['country'].apply(lambda x: x if x != 'Dominican Republic' else '')
    df['country'] = df['country'].apply(lambda x: x if x != 'DR Congo' else 'Democratic Republic of the Congo')
    df['country'] = df['country'].apply(lambda x: x if x != 'Dutch Guyana' else 'Guyana')
    df['country'] = df['country'].apply(lambda x: x if x != 'French Cameroons' else 'Cameroon')
    df['country'] = df['country'].apply(lambda x: x if x != 'Hati' else 'Haiti')
    df['country'] = df['country'].apply(lambda x: x if x != 'HI' else 'Hawaii')
    df['country'] = df['country'].apply(lambda x: x if x != 'HI)' else 'Hawaii')
    df['country'] = df['country'].apply(lambda x: x if x != 'Hunary' else 'Hungary')
    df['country'] = df['country'].apply(lambda x: x if x != 'Ilinois' else 'Illinois')
    df['country'] = df['country'].apply(lambda x: x if x != 'IN' else 'Indiana')
    df['country'] = df['country'].apply(lambda x: x if x != 'India.' else 'India')
    df['country'] = df['country'].apply(lambda x: x if x != 'Indian' else 'India')
    df['country'] = df['country'].apply(lambda x: x if x != 'Indiana' else '')
    df['country'] = df['country'].apply(lambda x: x if x != 'Inodnesia' else 'Indonesia')
    df['country'] = df['country'].apply(lambda x: x if x != 'Jamacia ' else 'Jamaica')
    df['country'] = df['country'].apply(lambda x: x if x != 'Khmer Republic' else 'Cambodia')
    df['country'] = df['country'].apply(lambda x: x if x != 'Louisana' else 'Louisiana')
    df['country'] = df['country'].apply(lambda x: x if x != 'Manmar' else 'Myanmar')
    df['country'] = df['country'].apply(lambda x: x if x != 'Massachutes' else 'Massachusetts')
    df['country'] = df['country'].apply(lambda x: x if x != 'Mexic' else 'Mexico')
    df['country'] = df['country'].apply(lambda x: x if x != 'Minnisota' else 'Minnesota')
    df['country'] = df['country'].apply(lambda x: x if x != 'Mississipi' else 'Mississippi')
    df['country'] = df['country'].apply(lambda x: x if x != 'Morroco' else 'Morocco')
    df['country'] = df['country'].apply(lambda x: x if x != 'Myanmar' else 'Burma')
    df['country'] = df['country'].apply(lambda x: x if x != 'Netherlands Antilles' else 'Netherlands')
    df['country'] = df['country'].apply(lambda x: x if x != 'Netherlands Indies' else 'Netherlands')
    df['country'] = df['country'].apply(lambda x: x if x != 'New York (Idlewild)' else 'New York')
    df['country'] = df['country'].apply(lambda x: x if x != 'NY' else 'New York')
    df['country'] = df['country'].apply(lambda x: x if x != 'Oklohoma ' else 'Oklahoma')
    df['country'] = df['country'].apply(lambda x: x if x != 'Papua' else 'Papua New Guinea')
    df['country'] = df['country'].apply(lambda x: x if x != 'Philipines' else 'Philippines')
    df['country'] = df['country'].apply(lambda x: x if x != 'Philippines' else 'Philippines')
    df['country'] = df['country'].apply(lambda x: x if x != 'Republic of Djibouti' else 'Djibouti')
    df['country'] = df['country'].apply(lambda x: x if x != 'Rhodesia (Zimbabwe)' else 'Zimbabwe')
    df['country'] = df['country'].apply(lambda x: x if x != 'Russian' else 'Russia')
    df['country'] = df['country'].apply(lambda x: x if x != 'Saint Lucia Island' else 'Saint Lucia')
    df['country'] = df['country'].apply(lambda x: x if x != 'Saudia Arabia' else 'Saudi Arabia')
    df['country'] = df['country'].apply(lambda x: x if x != 'Sierre Leone' else 'Sierra Leone')
    df['country'] = df['country'].apply(lambda x: x if x != 'South Dekota' else 'South Dakota')
    df['country'] = df['country'].apply(lambda x: x if x != 'South Korean' else 'South Korea')
    df['country'] = df['country'].apply(lambda x: x if x != 'South-West  Africa (Namibia)' else 'Namibia')
    df['country'] = df['country'].apply(lambda x: x if x != 'Soviet Union' else 'Russia')
    df['country'] = df['country'].apply(lambda x: x if x != 'Surinam' else 'Suriname')
    df['country'] = df['country'].apply(lambda x: x if x != 'Swden' else 'Sweden')
    df['country'] = df['country'].apply(lambda x: x if x != 'Taiwan (Formosa)' else 'Taiwan')
    df['country'] = df['country'].apply(lambda x: x if x != 'Tennesee' else 'Tennessee')
    df['country'] = df['country'].apply(lambda x: x if x != 'The Netherlands' else 'Netherlands')
    df['country'] = df['country'].apply(lambda x: x if x != 'UK' else 'United Kingdom')
    df['country'] = df['country'].apply(lambda x: x if x != 'Unied Kingdom' else 'United Kingdom')
    df['country'] = df['country'].apply(lambda x: x if x != 'US Virgin Islands' else 'U.S. Virgin Islands')
    df['country'] = df['country'].apply(lambda x: x if x != 'USSR' else 'Russia')
    df['country'] = df['country'].apply(lambda x: x if x != 'Uzbekstan' else 'Uzbekistan')
    df['country'] = df['country'].apply(lambda x: x if x != 'Virgin Islands' else 'U.S. Virgin Islands')
    df['country'] = df['country'].apply(lambda x: x if x != 'Virginia.' else 'Virginia')
    df['country'] = df['country'].apply(lambda x: x if x != 'Washingon' else 'Washington')
    df['country'] = df['country'].apply(lambda x: x if x != 'Washington DC' else 'Washington D.C.')
    df['country'] = df['country'].apply(lambda x: x if x != 'Wisconson' else 'Wisconsin')
    df['country'] = df['country'].apply(lambda x: x if x != 'WY' else 'Wyoming')
    df['country'] = df['country'].apply(lambda x: x if x != 'Yugosalvia' else 'Yugoslavia')
    df['country'] = df['country'].apply(lambda x: x if x != 'Zaïre' else 'Zaire')
    df['country'] = df['country'].apply(lambda x: x if x != 'Zimbabwe)' else 'Zimbabwe')
    df['country'] = df['country'].apply(lambda x: x if x != ': Massachusetts' else 'Massachusetts')
    df['country'] = df['country'].apply(lambda x: x if x != 'Barquisimeto Venezuela' else 'Venezuela')
    df['country'] = df['country'].apply(lambda x: x if x != 'Centeral Afghanistan\nAfghanistan' else 'Afghanistan')
    df['country'] = df['country'].apply(lambda x: x if x != 'Central Mozambique' else 'Mozambique')
    df['country'] = df['country'].apply(lambda x: x if x != 'Eastern Libya' else 'Libya')
    df['country'] = df['country'].apply(lambda x: x if x != 'Sint Maarten (Dutch part)' else 'Sint Maarten')
    #borramos "?" de todo el df
    df = df.replace('?', '')
    return df

def stats(df: pd.DataFrame):
    
    #numero de crashes por año en español
    print("Numero de accidentes por año: ", len(df))
    print("Total de fallecidos: ", df['fatalities'].sum())
    #total number of fatalities per year
    print("fallecidos por año: ")
    df_per_year = df.groupby(['year'])['fatalities'].agg(['sum', 'count', 'mean', 'max', 'min'])
    print(tabulate(df_per_year, headers=df_per_year.columns, tablefmt='orgtbl'))
    #total number of fatalities per month
    print("fallecidos por mes: ")
    df_per_month = df.groupby(['month'])['fatalities'].agg(['sum', 'count', 'mean', 'max', 'min'])
    print(tabulate(df_per_month, headers=df_per_month.columns, tablefmt='orgtbl'))
    #year with most fatalities epañol
    print("Año con mas fallecidos: ")
    print(df.groupby(['year'])['fatalities'].sum().idxmax())
    #year with least fatalities epañol
    print("Año con menos fallecidos: ")
    print(df.groupby(['year'])['fatalities'].sum().idxmin())
    #por aircraft type
    print("Fallecidos por aereonave:")
    df_per_type = df.groupby(['ac_type'])['fatalities'].agg(['sum', 'count', 'mean', 'max', 'min'])
    print(tabulate(df_per_type, headers=df_per_type.columns, tablefmt='orgtbl'))

def plot_data(df: pd.DataFrame):
    #accidentes por año
    df_per_year = df.groupby(['year'])['fatalities'].agg(['count'])
    df_per_year.plot(y = 'count',kind="bar", legend=False, figsize=(32,18),fontsize=15, title='Numero de accidentes por año')
    plt.savefig('Tarea-4/accidentes_por_año.png')
    plt.close()
    #accidentes por mes
    df_per_month = df.groupby(['month'])['fatalities'].agg(['count'])
    df_per_month.plot(y = 'count',kind="bar", legend=False, figsize=(32,18),fontsize=15, title='Numero de accidentes por mes')
    plt.savefig('Tarea-4/accidentes_por_mes.png')
    plt.close()
    #accidentes por tipo de aeronave
    df_per_type = df.groupby(['ac_type'])['fatalities'].agg(['count'])
    #ordenar por count
    df_per_type = df_per_type.sort_values(by=['count'], ascending=False)
    df_per_type = df_per_type.head(10)
    df_per_type.plot(y = 'count',kind="bar", legend=False, figsize=(32,18),fontsize=15, title='Numero de accidentes por tipo de aeronave')
    plt.savefig('Tarea-4/accidentes_por_tipo_de_aeronave.png')
    plt.close()
    #accidentes por pais
    df_per_country = df.groupby(['country'])['fatalities'].agg(['count'])
    #ordenar por count
    df_per_country = df_per_country.sort_values(by=['count'], ascending=False)
    df_per_country = df_per_country.head(30)
    df_per_country.plot(y = 'count',kind="bar", legend=False, figsize=(32,18),fontsize=15, title='Numero de accidentes por pais')
    plt.savefig('Tarea-4/accidentes_por_pais.png')
    plt.close()


def nova_test(df: pd.DataFrame):
    #por ejemplo comparar el año 2000 con el 2001 y ver si hay diferencia significativa en el numero de accidentes
    #numero de accidentes por año
    df_per_year = df.groupby(['year'])['fatalities'].agg(['count'])
    df_per_year = df_per_year.reset_index()
    #2000
    df_2000 = df_per_year.loc[df_per_year['year'] == 2000]
    #2001
    df_2001 = df_per_year.loc[df_per_year['year'] == 2001]
    #anova test
    print("ANOVA TEST")
    print("H0: mu_2000 = mu_2001")
    print("H1: mu_2000 != mu_2001")
    print("alpha = 0.05")
    print("p-value: ")
    print(anova_lm(ols('count ~ year', data=df_per_year).fit(), typ=2))
    if anova_lm(ols('count ~ year', data=df_per_year).fit(), typ=2).values[0][3] < 0.05:
        print("Reject H0")
    else:
        print("Fail to reject H0")
    

def main():
    data = clean_data(get_data2())
    #stats(data)
    #print_data(data)
    #plot_data(data)
    nova_test(data)
    save_data(data)

main()