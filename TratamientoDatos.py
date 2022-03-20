import numpy as np
import pandas as pd
import pickle
import random
import datetime as dt
from time import process_time
#import multiprocessing as mp
#from multiprocessing import Pool
#import funcionesAuxiliares as funciones
from tqdm import tqdm

#!pip3 install pickle5
#import pickle5 as pickle

fichero = open('./Datos/navs.pickle','rb')
# Cargamos los datos del fichero
lista_fichero = pickle.load(fichero)
#Cerramos
fichero.close()




maestroValores = pd.read_csv('./Datos/maestro.csv') #cargamos el maestro de valores

#Conseguimos todos los identificadores de allfunds_id del maestro de valores y declaramos el vector de fechas (el cual se contempla desde 05/01/2016 y 16/07/2021).
identificadores = maestroValores.loc[:,'allfunds_id']
fechas = pd.date_range(start="2016-01-05",end='2021-07-16', freq='B')

dataframeCompleto = pd.DataFrame(np.zeros((fechas.shape[0], identificadores.shape[0])),index=fechas,columns=identificadores)

for allfunds_id in lista_fichero.keys():
    dataframeCompleto.loc[:,allfunds_id] = lista_fichero[allfunds_id].nav

#Tomamos aquellos fondos los cuales tengan MENOS de 100 datos con NA, posteriormente rellenamos los datos que tienen NA y obtenemos un dataframe con información completa.
dataframeCompleto = dataframeCompleto.loc[:,dataframeCompleto.isna().sum(axis=0)<100]
dataframeCompleto = dataframeCompleto.fillna(method = 'ffill')
dataframeCompleto = dataframeCompleto.fillna(method = 'bfill')

#quito los fondos con todos sus nav a 0
fondosSinRegistro = dataframeCompleto.columns[dataframeCompleto.sum(axis=0)==0]
dataframeCompleto=dataframeCompleto.drop(fondosSinRegistro, axis=1)
dataframeCompletoValores = dataframeCompleto.values

MSCI = pd.read_csv('./Datos/MSCI.csv', sep=";",index_col=0, parse_dates=True,nrows=dataframeCompleto.shape[0])
MSCI = MSCI.fillna(method = 'ffill')

dataframeCompleto.to_csv('datos.csv')



