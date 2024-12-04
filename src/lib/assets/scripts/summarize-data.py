# This script generates a json file with all data summaries related to the svelte project
import pandas as pd
import json

# output json file
OUTPUT_PATH = "./src/lib/data/"
OUTPUT_JSON = 'data_summaries.json'
 
# The path is different in python in comparison with JS: it is the project path
FILE = "./static/data/output/long_data_with_cantonId.csv"
FILE1 = "./static/data/support/age_range.csv"
FILE2 = "./static/data/support/proyeccion_cantonal_total_2010-2020.csv"
FILE3 = "./static/data/support/categories.csv"

df = pd.read_csv(FILE, dtype={'areacd': 'str'})
df1 = pd.read_csv(FILE1)
df2 = pd.read_csv(FILE2, dtype={'Codigo': 'str'})
df3 = pd.read_csv(FILE3)

## fill data for missing years and unpivot projection population
maxYearData = df['disappearance_year'].max()
years = df2.filter(like='20').columns.to_list()
years = [int(x) for x in years]
maxYearProjection = max(years)
missingYears = list(range(maxYearProjection + 1, maxYearData + 1))
df2.columns = [x.lower() for x in df2.columns]
df2.rename(columns=lambda x: 'P' + x if x.startswith('20') else x, inplace=True)
df2.rename(columns={'codigo': 'cantonId', 'nombre de canton': 'cantonName'}, inplace=True)
for i in missingYears:
  df2['P' + str(i)] = df2['P' + str(maxYearProjection)]
df2 = pd.wide_to_long(df2, stubnames='P', i=['cantonId', 'cantonName'], j='year').reset_index()
df2.rename(columns={'P': 'proj_population'}, inplace=True)

# join
all_data = pd.merge(df, df3, on='motivo_desaparicion_obs', how='left')

# aggregations
agg_by_age_range = all_data.groupby(['country', 'rango_edad']).size().reset_index(name='count')
agg_by_age_range['percentage'] = 100 * (agg_by_age_range['count'] / agg_by_age_range['count'].sum())
agg_by_age_range.rename(columns={'rango_edad': 'cardinality'}, inplace=True)

agg_by_year = all_data.groupby(['country', 'disappearance_year']).size().reset_index(name='count')
agg_by_year['percentage'] = 100 * (agg_by_year['count'] / agg_by_year['count'].sum())
agg_by_year['disappearance_year'] = agg_by_year['disappearance_year'].astype(str)
agg_by_year.rename(columns={'disappearance_year': 'cardinality'}, inplace=True)

agg_by_tipology = all_data.groupby(['country', 'tipology']).size().reset_index(name='count')
agg_by_tipology['percentage'] = 100 * (agg_by_tipology['count'] / agg_by_tipology['count'].sum())
agg_by_tipology.rename(columns={'tipology': 'cardinality'}, inplace=True)

agg_by_category = all_data.groupby(['country', 'category']).size().reset_index(name='count')
agg_by_category['percentage'] = 100 * (agg_by_category['count'] / agg_by_category['count'].sum())
agg_by_category.rename(columns={'category': 'cardinality'}, inplace=True)

agg_by_sex = all_data.groupby(['country', 'sexo']).size().reset_index(name='count')
agg_by_sex['percentage'] = 100 * (agg_by_sex['count'] / agg_by_sex['count'].sum())
agg_by_sex.rename(columns={'sexo': 'cardinality'}, inplace=True)

agg_by_canton = all_data.groupby(['country', 'disappearance_year','areacd']).size().reset_index(name='missed')
agg_by_canton = agg_by_canton.merge(df2, how='left', left_on=['areacd', 'disappearance_year'],right_on=['cantonId', 'year'])
agg_by_canton['missedPer10k'] = agg_by_canton['missed'] / agg_by_canton['proj_population'] * 10000
agg_by_canton.drop(columns=['proj_population', 'cantonId', 'cantonName'], inplace=True) 
agg_by_canton.rename(columns={'areacd': 'cantonId'}, inplace=True) 

# convert multidataframes to json
map_summaries = {'age_range': agg_by_age_range, 
                 'disappearance_year': agg_by_year, 
                 'tipology': agg_by_tipology, 
                 'category': agg_by_category, 
                 'sex': agg_by_sex,
                 'canton': agg_by_canton
                 }
summaries = []
for k,v in map_summaries.items():
  row_summary = {}
  column = v.columns.to_list()[1]
  row_summary['kpi'] = k
  # this is the key. to_json method return str so you have to reconvert to a list with json.loads. finally when you dump it doesn't display with "\"
  row_summary['data'] = json.loads(v.to_json(orient='records'))
  summaries.append(row_summary)

with open(OUTPUT_PATH + OUTPUT_JSON, 'w') as f:
  json.dump(summaries, f)

# agg_by_canton.to_csv(OUTPUT_PATH + 'canton.csv', index=False)
print('JSON file created.')