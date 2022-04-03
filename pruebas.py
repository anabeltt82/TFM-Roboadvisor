import pandas as pd
import numpy as np
import PreparaDatos as PrepDatos

Datos = PrepDatos.PreparaDatos()


print(Datos.maestro[:100])


#inspeccionamos el maestro para ver que datos contiene
# isin
# allfunds_id
# asset
# asset_type **
# class_code
# clean_share
# currency
# geo_area
# geo_zone
# inception_at
# income
# management_fee
# manager_id
# manager_name
# name
# ongoing_charges


asset_class = {
        'ABR': 'alternative', 'ACF': 'alternative', 'ACU': 'alternative', 'AED': 'alternative', 'AGM': 'alternative', 'ALS': 'alternative',
        'ALT': 'alternative', 'AMF': 'alternative', 'AMS': 'alternative', 'ARV': 'alternative', 'BAL': 'mixed', 'BIN': 'equity', 'BIO': 'equity',
        'COM': 'other', 'CON': 'fixed_income', 'COR': 'fixed_income', 'COS': 'equity', 'DCO': 'equity', 'DEF': 'mixed', 'DRS': 'alternative',
        'DYN': 'mixed', 'EM': 'fixed_income', 'FIN': 'equity', 'FLE': 'mixed', 'GAR': 'fixed_income', 'GOL': 'equity', 'GOV': 'fixed_income',
        'HDG': 'alternative', 'HEA': 'equity', 'HY': 'fixed_income', 'IDT': 'equity', 'INF': 'fixed_income', 'MX': 'equity', 'MMD': 'money',
        'MMK': 'money', 'NEU': 'alternative', 'NAR': 'equity', 'RFG': 'fixed_income', 'RFL': 'fixed_income', 'RFM': 'fixed_income', 'RFS': 'fixed_income',
        'RST': 'equity', 'RVA': 'equity', 'RVG': 'equity', 'SMD': 'equity', 'TEC': 'equity', 'TEL': 'equity', 'TMA': 'mixed', 'UTI': 'equity', 'OTH': 'mixed', 'OTS': 'mixed',
    }

family = {
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
    }

subcategory = {
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
    }

full_name = {
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
}

nested_family = {
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
    }
print(Datos.activosDisponibles)


