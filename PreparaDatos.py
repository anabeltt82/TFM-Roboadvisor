
import random
import pandas as pd
import numpy as np
from tqdm import tqdm
import time
import pickle




class PreparaDatos():
    """Esta clase se utiliza para que los monos reutilicen los datos necesarios
    y no tener que calcular permanentemente datos o usar variables globales.
    Se pasa como parámetro a todos los monos.
    """
    # Semilla números aleatorios
    #    np.random.seed(42)
    # Preparación de datos de activos
    #   reinversion = True
    # Pruebas
    test = False
    # Ventana de volatilidad rolling
    ventanaVola = 4  # 30
 
    def __init__(self) -> None:
        if (self.test == True):
            # Cargamos datos ya tratados para ahorrar tiempo
            self.allData = self.cargarDatosTratados()

        else:
            self.maestro, self.navs_dict = self.cargarDatosRaw()
            self.allData = self.homogeneizarDatosActivos(self.navs_dict)
            self.allData = self.normalizarDatos(self.allData)
            # Guardamos datos tratados para ahorrar tiempo
            self.allData.to_csv("./Datos/allData.csv")

        # Rentabilidad de los activos
        self.allRentab = self.calcularRentabilidadActivos(self.allData)
        # Ids de los activos diponibles
        self.activosDisponibles = range(len(self.allRentab.columns))

        # Preparación de datos de índice
        self.indice = self.cargarIndice().sort_index(axis=0, ascending=True)
        self.indice = self.homogeneizarDatosIndice(data=self.indice)
        self.indice = self.indice.loc[self.allData.index, :]
        self.indice = self.normalizarDatos(self.indice)

        # Renta fija - Suponemos cero
        self.rf = pd.DataFrame(np.zeros(len(self.indice)))

        # Vola Rolling
        self.allVolaRolling = np.sqrt(
            self.allRentab.rolling(self.ventanaVola).var())

        # Pasamos a NumPy para optimizar rendimiento
        self.allData = self.allData.to_numpy()
        self.allRentab = self.allRentab.to_numpy()
        self.rf = self.rf.to_numpy()
        self.allVolaRolling = self.allVolaRolling.to_numpy()
        #self.allAlphaJensen = self.allAlphaJensen.to_numpy()
        self.indice = self.indice.to_numpy()

    def cargarDatosRaw(self) -> tuple:
        maestro = pd.read_csv(
            "./Datos/maestro.csv",
            usecols=["allfunds_id", "asset", "geo_area",
                     "management_fee", "manager_id", "ongoing_charges"],
            index_col="allfunds_id")

        navs_dict = dict(pickle.load(
            open("./Datos/navs.pickle", "rb")))

        return (maestro, navs_dict)

    def cargarIndice(self) -> pd.DataFrame:
        msci = pd.read_csv(
            "./Datos/MSCI_World_Investing.csv",
            usecols=["Fecha", "Último"],
            index_col="Fecha",
            parse_dates=True,
            dayfirst=True,
            decimal=",",
            thousands=".",
            dtype={"Último": np.float64})
        msci.columns = ["close"]
        msci.index.name = "date"

        return msci

    def homogeneizarDatosIndice(self, data: pd.DataFrame) -> pd.DataFrame:
        # Homogeneizamos, limpiamos y devolvemos datos semanales
        # Eliminamos fines de semana
        data = data.drop(
            labels=data.index[data.index.weekday > 5],
            axis=0)

        # Remuestreo semanal y calculamos OHLC
        data = data.resample(rule="W-MON").ohlc()

        # Nos quedamos con el precio de cierre del intervalo
        data = data.loc[:, pd.IndexSlice[:, ['close']]]

        # Descartamos el nivel del multi-index que no nos interesa
        data.columns = data.columns.droplevel(level=1)

        return (data)

    def homogeneizarDatosActivos(self, navs_dict: dict) -> pd.DataFrame:
        # Homogeneizamos, limpiamos y devolvemos datos semanales
        
        # Las claves del diccionario son los Ids de AllFunds
        allData = pd.concat(navs_dict.values())

        # Tomamos la fecha, el identificador del fondo y el vl
        # Pasamos de formato largo a ancho
        allData = allData.pivot(columns='allfunds_id', values='nav')

        # Eliminamos fines de semana
        allData = allData.drop(
            labels=allData.index[allData.index.weekday > 5],
            axis=0)

        # Descartamos las filas con más de un 90% de NaN
        diasNoEliminar = ~(allData.isna().sum(
            axis=1) > allData.shape[1] * 0.9)
        allData = allData.loc[diasNoEliminar, :]

        # Rellenamos hacia adelante los datos faltantes con un máximo de 5 datos consecutivos
        # allData = allData.fillna(
        #    method="ffill",
        #    axis=1,
        #    limit=5)

        # Rellenamos hacia atrás los datos faltantes
        # allData = allData.fillna(
        #    method="bfill",
        #    axis=1)

        # Remuestreo semanal y calculamos OHLC
        # con el objetivo de tener datos para todos los activos
        allData = allData.resample(rule="W-MON").ohlc()

        # Nos quedamos con el precio de cierre del intervalo
        allData = allData.loc[:, pd.IndexSlice[:, ['close']]]

        # Descartamos activos con NA
        allData = allData.T.dropna(axis=0)

        # Descartamos el nivel del multi-index que no nos interesa
        allData.index = allData.index.droplevel(level=1)

        return (allData.T)

    def normalizarDatos(self, data: pd.DataFrame) -> pd.DataFrame:
        # Normalizamos los datos para poder compararlos
        data = data.iloc[:, :] / data.iloc[0, :]
        return (data)

    def cargarDatosTratados(self) -> pd.DataFrame:
        data = pd.read_csv(
            "./Datos/allData.csv",
            index_col="date",
            parse_dates=True)
        return data

    def calcularRentabilidadActivos(self, data: pd.DataFrame) -> pd.DataFrame:
        rentab = np.log(data).diff()
        rentab = rentab.fillna(value=0)

        return rentab