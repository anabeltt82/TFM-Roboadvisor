import pandas as pd
import numpy as np
import PreparaDatos as PrepDatos

Datos = PrepDatos.PreparaDatos()


print(Datos.maestro[:100])
Datos.maestro.to_csv("C:/Users/anabe/OneDrive/Documentos/master miaX/TFM_Anabel/Anabel TFM/Datos/prueba.csv")

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


#print(Datos.activosDisponibles)

#df = pd.DataFrame(Datos.activosDisponibles)


