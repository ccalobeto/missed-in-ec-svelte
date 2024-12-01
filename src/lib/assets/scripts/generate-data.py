# This script generates a csv cleaned file with accumulated data.
import pandas as pd
import numpy as np
import unidecode

# The path is different in python in comparison with JS: it is the project path
FILE = "./static/data/input/mdi_personas_desaparecidas_2017-2023.csv"
FILE1 = "./static/data/input/mdi_personas_desaparecidas_2024_enero-octubre.csv"
df = pd.read_csv(FILE)
df1 = pd.read_csv(FILE1)

# rename columns
newColumns = {
  'edad_aproximada': 'edad',
  'motivo_desaparcion': 'motivo_desaparicion',
  'motivo_desaparcion_observada': 'motivo_desaparicion_obs',
}
newColumns1 = {
  'latitud_desaparicion': 'latitud',
  'longitud_desaparicion': 'longitud',
  'edad_aproximada': 'edad',
  'motivo_desaparcion': 'motivo_desaparicion',
  'motivo_desaparcion_observada': 'motivo_desaparicion_obs',
}
df.rename(columns=newColumns, inplace=True)
df1.rename(columns=newColumns1, inplace=True)

# reorder columns for df1
df1 = df1[['provincia', 'latitud', 'longitud', 'edad', 'sexo', 'motivo_desaparicion', 'motivo_desaparicion_obs', 'fecha_desaparicion', 'situacion_actual', 'fecha_localizacion', 'rango_edad', 'latitud_encontrado', 'longitud_encontrado']]

# reemplace SIN_DATO with NaN
df.replace('SIN_DATO', np.nan, inplace=True)
df1.replace('SIN_DATO', np.nan, inplace=True)
# do some cleaning and transform. Only float accept nan values
df['edad'] = df['edad'].astype('float32')
df['motivo_desaparicion_obs'] = df['motivo_desaparicion_obs'].str.upper()
df1['edad'] = df1['edad'].astype('float32')
df1['motivo_desaparicion_obs'] = df1['motivo_desaparicion_obs'].str.upper()
df1['rango_edad'] = df1['rango_edad'].str.upper().map({'PERSONAS DE LA TERCERA EDAD': 'TERCERA EDAD'})
df1['latitud_encontrado'] = df1['latitud_encontrado'].astype('float32')
df1['longitud_encontrado'] = df1['longitud_encontrado'].astype('float32')

## add categories to df
bins = [-1, 12, 17, 24, 35, 50, 64, np.inf]
labels = ['NIÑOS', 'ADOLESCENTES', 'JÓVENES ADULTOS', 'ADULTOS JÓVENES', 'ADULTOS', 'ADULTOS MAYORES', 'TERCERA EDAD']
df['rango_edad'] = pd.cut(df['edad'], bins, labels=labels)

# transform to string date to date
df['fecha_desaparicion'] = pd.to_datetime(df['fecha_desaparicion'], format='%d/%m/%Y')
df['fecha_localizacion'] = pd.to_datetime(df['fecha_localizacion'], format='%d/%m/%Y')
df1['fecha_desaparicion'] = pd.to_datetime(df1['fecha_desaparicion'], format='%d/%m/%Y')
df1['fecha_localizacion'] = pd.to_datetime(df1['fecha_localizacion'], format='%d/%m/%Y')

# Append dfs
df2 = pd.concat([df, df1], ignore_index=True)

# fill missing values of edadwith the mean
meanAgeOfYoungAdults = df2[df2['rango_edad']=='ADULTOS JÓVENES']['edad'].mean()
df2.loc[df2['edad'].isna(), 'edad'] = meanAgeOfYoungAdults
# fill missing values of rango_edad
df2.loc[df2['rango_edad'].isna(),'rango_edad'] = pd.cut(df2['edad'], bins, labels=labels)

# add extra columns for analysis
df2['disappearance_year'] = df2['fecha_desaparicion'].dt.year
df2['disappearance_month'] = df2['fecha_desaparicion'].dt.month
df2['disappearance_day'] = df2['fecha_desaparicion'].dt.day
df2['days_gone'] = (df2['fecha_localizacion'] - df2['fecha_desaparicion']).dt.days
# add country ISO 3166-1 A-3 code
df2['country'] = 'ECU'

# remove accents
cols_accents_to_remove = ['motivo_desaparicion', 'motivo_desaparicion_obs', 'rango_edad']
for column in cols_accents_to_remove:
  df2[column] = df2[column].apply(lambda x: unidecode.unidecode(x) if x is not np.nan else x)

# dataframe statistics
# print('shape: ', df2.shape)
# print('columns: ', df2.columns)
# print('summary: ', df2.describe())
# print('dtypes: ', df2.dtypes)
# print('NaN values', df2.isna().sum())
# print(df2[df2['motivo_desaparicion']=='CAUSAS SOCIALES'].iloc[:, 10:])
# print(meanAgeOfYoungAdults)

# save
df2.to_csv('./static/data/output/long_data.csv', index=False)