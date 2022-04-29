
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
        self.path_datos = "C:/Users/anabe/OneDrive/Documentos/master miaX/TFM_Anabel/Anabel TFM/Datos"
        if (self.test == True):
            # Cargamos datos ya tratados para ahorrar tiempo
            self.allData = self.cargarDatosTratados()

        else:
            self.maestro, self.navs_dict = self.cargarDatosRaw()
            self.maestro = self.mapeaMaestro(self.maestro)
            self.allData = self.homogeneizarDatosActivos(self.navs_dict)
            self.allData = self.normalizarDatos(self.allData)
            # Guardamos datos tratados para ahorrar tiempo
            self.allData.to_csv(self.path_datos + "/allData.csv")

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
            self.path_datos + "/maestro.csv",
            usecols=["allfunds_id", "asset", "asset_type", "geo_area", "geo_zone",
                     "management_fee", "manager_id", "ongoing_charges"],
            index_col="allfunds_id")

        navs_dict = dict(pickle.load(
            open(self.path_datos + "/navs.pickle", "rb")))

        return (maestro, navs_dict)
    
    def mapeaMaestro(self, data: pd.DataFrame) -> pd.DataFrame:
        data['asset_class']=data['asset_type'].map({ 
        'ABR': 'alternative', 'ACF': 'alternative', 'ACU': 'alternative', 'AED': 'alternative', 'AGM': 'alternative', 'ALS': 'alternative',
        'ALT': 'alternative', 'AMF': 'alternative', 'AMS': 'alternative', 'ARV': 'alternative', 'BAL': 'mixed', 'BIN': 'equity', 'BIO': 'equity',
        'COM': 'other', 'CON': 'fixed_income', 'COR': 'fixed_income', 'COS': 'equity', 'DCO': 'equity', 'DEF': 'mixed', 'DRS': 'alternative',
        'DYN': 'mixed', 'EM': 'fixed_income', 'FIN': 'equity', 'FLE': 'mixed', 'GAR': 'fixed_income', 'GOL': 'equity', 'GOV': 'fixed_income',
        'HDG': 'alternative', 'HEA': 'equity', 'HY': 'fixed_income', 'IDT': 'equity', 'INF': 'fixed_income', 'MX': 'equity', 'MMD': 'money',
        'MMK': 'money', 'NEU': 'alternative', 'NAR': 'equity', 'RFG': 'fixed_income', 'RFL': 'fixed_income', 'RFM': 'fixed_income', 'RFS': 'fixed_income',
        'RST': 'equity', 'RVA': 'equity', 'RVG': 'equity', 'SMD': 'equity', 'TEC': 'equity', 'TEL': 'equity', 'TMA': 'mixed', 'UTI': 'equity', 'OTH': 'mixed', 'OTS': 'mixed',
        })
        data['family']=data['asset_type'].map({
        'ABR': 'retorno absoluto', 'ACF': 'renta variable ocde', 'ACU': 'renta variable ocde', 'AED': 'renta variable ocde', 'AGM': 'renta variable ocde',
        'ALS': 'renta variable ocde', 'ALT': 'renta variable ocde', 'AMF': 'renta variable ocde', 'AMS': 'renta variable ocde', 'ARV': 'renta variable ocde',
        'BAL': 'deuda corporativa grado de inversion', 'BIN': 'renta variable ocde', 'BIO': 'renta variable ocde', 'COM': 'commodities', 'CON': 'convertibles',
        'COR': 'deuda corporativa grado de inversion', 'COS': 'renta variable ocde', 'DCO': 'renta variable ocde', 'DEF': 'deuda publica ocde', 'DRS': 'inmobiliario',
        'DYN': 'renta variable emergentes', 'EM': 'bonos high yield', 'FIN': 'renta variable ocde', 'FLE': 'renta variable ocde', 'GAR': 'retorno absoluto',
        'GOL': 'renta variable ocde', 'GOV': 'deuda publica ocde', 'HDG': 'retorno absoluto', 'HEA': 'renta variable ocde', 'HY': 'bonos high yield', 'IDT': 'renta variable ocde',
        'INF': 'deuda corporativa grado de inversion', 'MMD': 'liquidez y renta fija a corto plazo', 'MMK': 'liquidez y renta fija a corto plazo', 'MX': 'renta variable emergentes',
        'NAR': 'renta variable ocde', 'NEU': 'retorno absoluto', 'RFG': 'deuda corporativa grado de inversion', 'RFL': 'deuda corporativa grado de inversion',
        'RFM': 'deuda corporativa grado de inversion', 'RFS': 'deuda corporativa grado de inversion', 'RST': 'renta variable ocde', 'RVA': 'ver zona geografica',
        'RVG': 'ver zona geografica', 'SMD': 'ver zona geografica', 'TEC': 'renta variable ocde', 'TEL': 'renta variable ocde', 'TMA': 'deuda publica ocde',
        'UTI': 'renta variable ocde', 'OTH': 'renta variable ocde', 'OTS': 'renta variable ocde',
        })
        data['subcategory']=data['asset_type'].map({
        'ABR': 'alternativos_liquidos', 'ACF': 'alternativos_liquidos', 'ACU': 'alternativos_liquidos', 'AED': 'alternativos_liquidos', 'AGM': 'alternativos_liquidos',
        'ALS': 'alternativos_liquidos', 'ALT': 'alternativos_liquidos', 'AMF': 'alternativos_liquidos', 'AMS': 'alternativos_liquidos', 'ARV': 'alternativos_liquidos',
        'BAL': 'mixtos_equilibrado', 'BIN': 'renta_variable_sectorial', 'BIO': 'renta_variable_sectorial', 'COM': 'otros', 'CON': 'renta_fija_convertibles',
        'COR': 'renta_fija_largo_plazo', 'COS': 'renta_variable_sectorial', 'DCO': 'renta_variable_sectorial', 'DEF': 'mixtos_conservador', 'DRS': 'alternativos_inmobiliario',
        'DYN': 'mixtos_agresivos', 'EM': 'renta_fija_emergente', 'FIN': 'renta_variable_sectorial', 'FLE': 'mixto_flexible', 'GAR': 'renta_fija_largo_plazo',
        'GOL': 'renta_variable_sectorial', 'GOV': 'renta_fija_largo_plazo', 'HDG': 'alternativos_liquidos', 'HEA': 'renta_variable_sectorial', 'HY': 'renta_fija_high_yield',
        'IDT': 'renta_variable_sectorial', 'INF': 'renta_fija_largo_plazo', 'MMD': 'monetario', 'MMK': 'monetario', 'MX': 'ver_zona_geografica', 
        'NAR': 'renta_variable_sectorial', 'NEU': 'alternativos_liquidos', 'RFG': 'renta_fija_largo_plazo', 'RFL': 'renta_fija_largo_plazo', 
        'RFM': 'renta_fija_corto_y_medio_plazo', 'RFS': 'renta_fija_corto_y_medio_plazo', 'RST': 'renta_variable_sectorial', 'RVA': 'ver_zona_geografica', 
        'RVG': 'ver_zona_geografica', 'SMD': 'ver_zona_geografica', 'TEC': 'renta_variable_sectorial', 'TEL': 'renta_variable_sectorial', 'TMA': 'mixtos_equilibrado', 
        'UTI': 'renta_variable_sectorial', 'OTH': 'mixto_flexible', 'OTS': 'mixto_flexible',
        })
        data['full_name']=data['geo_zone'].map({
        'BR': 'BRASIL', 'CA': 'CANADA', 'CAR': 'CARIBE', 'CL': 'CHILE', 'LAM': 'LATINOAMERICA MISC', 'LAT': 'LATINOAMERICA', 'MX': 'MEXICO', 'PAM': 'PANAMERICA', 
        'US': 'USA', 'ASE': 'ASIAN', 'ASP': 'ASIA PASIFICO', 'ATA': 'AUSTRALASIA', 'AU': 'AUSTRALIA', 'AXJ': 'ASIA EX JAPON', 'B': 'BAHREIN', 'CHI': 'CHINA', 
        'EAU': 'EMIRATOS ARABES UNIDOS', 'EGY': 'EGIPTO', 'EIJ': 'FAR EAST', 'EXJ': 'FAST EAST EX-JAPON', 'GCC': 'GCC', 'GCH': 'GREATER CHINA', 'HK': 'HONG KONG', 
        'IL': 'ISRAEL', 'IN': 'INDIA', 'IND': 'INDONESIA', 'JO': 'JORDANIA', 'JP': 'JAPON', 'KR': 'KOREA', 'KWT': 'KUWAIT', 'LE': 'LIBANO', 'MDE': 'ORIENTE MEDIO',
        'MNA': 'MENA', 'MO': 'MARRUECOS', 'MSA': 'MALASIA', 'OM': 'OMAN', 'PH': 'FILIPINAS', 'SAU': 'ARABIA SAUDITA', 'SG': 'SINGAPUR', 
        'SYM': 'SINGAPUR Y MALASIA', 'TH': 'THAILANDIA', 'TU': 'TUNEZ', 'TW': 'TAIWAN', 'VNM': 'VIETNAM', 'AT': 'AUSTRIA', 'BA': 'PAISES BALTICOS', 'BE': 'BELGICA', 
        'BNL': 'BENELUX', 'CH': 'SUIZA', 'CZE': 'REPUBLICA CHECA', 'DE': 'ALEMANIA', 'DK': 'DINAMARCA', 'EE': 'EUROPA EMERGENTE',
        'EES': 'EUROPA EXSUIZA', 'EMI': 'EUROPA MISC', 'ES': 'ESPAÑA', 'EU': 'EUROPA', 'EUK': 'EUROPA EX-UK', 'EUR': 'ZONA EURO', 'FI': 'FINLANDIA', 'FR': 'FRANCIA', 
        'GR': 'GRECIA', 'HUN': 'HUNGRIA', 'IBE': 'IBERICA', 'IE': 'IRLANDA', 'ISL': 'ISLANDIA', 'IT': 'ITALIA', 'LIE': 'LIETCHTENSTEIN', 'LUX': 'LUXEMBURGO', 
        'LU': 'LUXEMBURGO', 'MLT': 'MALTA', 'NL': 'PAISES BAJOS', 'NO': 'NORUEGA', 'NOR': 'PAISES NORDICOS', 'POL': 'POLONIA', 'PT': 'PORTUGAL', 'RS': 'RUSIA', 
        'SE': 'SUECIA', 'SKA': 'ESCANDINAVIA', 'SVK': 'ESLOVAQUIA', 'TR': 'TURQUIA', 'UK': 'REINO UNIDO', 'GB': 'REINO UNIDO', 'AFR': 'AFRICA', 'BRC': 'BRIC',
        'GEA': 'GLOBAL EX AUSTRALIA', 'GEM': 'GLOBAL EMERGENTE', 'GEU': 'GLOBAL EX-US', 'GLB': 'GLOBAL', 'NZL': 'NUEVA ZELANDA', 'SAF': 'SUDAFRICA', 'EME': 'EMEA'
        })
        data['nested_family']=data['geo_zone'].map({
        'BR': 'renta variable emergentes', 'CA': 'renta variable ocde', 'CAR': 'renta variable emergentes', 'CL': 'renta variable emergentes', 
        'LAM': 'renta variable emergentes', 'LAT': 'renta variable emergentes', 'MX': 'renta variable emergentes', 'PAM': 'renta variable emergentes', 
        'US': 'renta variable ocde', 'ASE': 'renta variable emergentes', 'ASP': 'renta variable emergentes', 'ATA': 'renta variable emergentes', 'AU': 'renta variable ocde', 
        'AXJ': 'renta variable emergentes', 'B': 'renta variable emergentes', 'CHI': 'renta variable emergentes', 'EAU': 'renta variable emergentes', 
        'EGY': 'renta variable emergentes', 'EIJ': 'renta variable emergentes', 'EXJ': 'renta variable emergentes', 'GCC': 'renta variable emergentes', 
        'GCH': 'renta variable emergentes', 'HK': 'renta variable emergentes', 'IL': 'renta variable emergentes', 'IN': 'renta variable emergentes',
        'IND': 'renta variable emergentes', 'JO': 'renta variable emergentes', 'JP': 'renta variable emergentes', 'KR': 'renta variable emergentes', 
        'KWT': 'renta variable emergentes', 'LE': 'renta variable emergentes', 'MDE': 'renta variable emergentes', 'MNA': 'renta variable emergentes', 
        'MO': 'renta variable emergentes', 'MSA': 'renta variable emergentes', 'OM': 'renta variable emergentes', 'PH': 'renta variable emergentes', 
        'SAU': 'renta variable emergentes', 'SG': 'renta variable emergentes', 'SYM': 'renta variable emergentes', 'TH': 'renta variable emergentes', 
        'TU': 'renta variable emergentes', 'TW': 'renta variable emergentes', 'VNM': 'renta variable emergentes', 'AT': 'renta variable ocde',
        'BA': 'renta variable emergentes', 'BE': 'renta variable ocde', 'BNL': 'renta variable ocde', 'CH': 'renta variable ocde', 'CZE': 'renta variable ocde', 
        'DE': 'renta variable ocde', 'DK': 'renta variable ocde', 'EE': 'renta variable emergentes', 'EES': 'renta variable ocde', 'EMI': 'renta variable ocde', 
        'ES': 'renta variable ocde', 'EU': 'renta variable ocde', 'EUK': 'renta variable ocde', 'EUR': 'renta variable ocde', 'FI': 'renta variable ocde', 
        'FR': 'renta variable ocde', 'GR': 'renta variable ocde', 'HUN': 'renta variable ocde', 'IBE': 'renta variable ocde', 'IE': 'renta variable ocde', 
        'ISL': 'renta variable ocde', 'IT': 'renta variable ocde', 'LIE': 'renta variable ocde', 'LUX': 'renta variable ocde', 'LU': 'renta variable ocde', 
        'MLT': 'renta variable ocde', 'NL': 'renta variable ocde', 'NO': 'renta variable ocde', 'NOR': 'renta variable ocde', 'POL': 'renta variable ocde',
        'PT': 'renta variable ocde', 'RS': 'renta variable emergentes', 'SE': 'renta variable ocde', 'SKA': 'renta variable ocde', 'SVK': 'renta variable ocde', 
        'TR': 'renta variable emergentes', 'UK': 'renta variable ocde', 'GB': 'renta variable ocde', 'AFR': 'renta variable emergentes', 'BRC': 'renta variable emergentes', 
        'GEA': 'renta variable ocde', 'GEM': 'renta variable emergentes', 'GEU': 'renta variable ocde', 'GLB': 'renta variable ocde', 'NZL': 'renta variable ocde', 
        'SAF': 'renta variable emergentes', 'EME': 'renta variable ocde'
        })
        return (data)

    def cargarIndice(self) -> pd.DataFrame:
        msci = pd.read_csv(
            self.path_datos +"/MSCI_World_Investing.csv",
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
            self.path_datos + "/allData.csv",
            index_col="date",
            parse_dates=True)
        return data

    def calcularRentabilidadActivos(self, data: pd.DataFrame) -> pd.DataFrame:
        rentab = np.log(data).diff()
        rentab = rentab.fillna(value=0)

        return rentab