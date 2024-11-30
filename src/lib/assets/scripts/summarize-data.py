# This script generates a json file with all summaries for your svelte project
import pandas as pd
import unidecode
import json

# output json file
OUTPUT = "./static/data/output/data_summaries.json"
 
# The path is different in python in comparison with JS: it is the project path
FILE = "./static/data/output/long_data.csv"
FILE1 = "./static/data/support/age_range.csv"
FILE2 = "./static/data/support/proyeccion_cantonal_total_2010-2020.csv"
FILE3 = "./static/data/support/categories.csv"

df = pd.read_csv(FILE)
df1 = pd.read_csv(FILE1)
df2 = pd.read_csv(FILE2)
df3 = pd.read_csv(FILE3)

# join
all_data = pd.merge(df, df3, on='motivo_desaparicion_obs', how='left')

# aggregations
agg_by_age_range = all_data.groupby('rango_edad').size().reset_index(name='count')
agg_by_age_range['percentage'] = 100 * (agg_by_age_range['count'] / agg_by_age_range['count'].sum())

agg_by_year = all_data.groupby('disappearance_year').size().reset_index(name='count')
agg_by_year['percentage'] = 100 * (agg_by_year['count'] / agg_by_year['count'].sum())
agg_by_year['disappearance_year'] = agg_by_year['disappearance_year'].astype(str)

agg_by_tipology = all_data.groupby('tipology').size().reset_index(name='count')
agg_by_tipology['percentage'] = 100 * (agg_by_tipology['count'] / agg_by_tipology['count'].sum())

agg_by_category = all_data.groupby('category').size().reset_index(name='count')
agg_by_category['percentage'] = 100 * (agg_by_category['count'] / agg_by_category['count'].sum())

agg_by_sex = all_data.groupby('sexo').size().reset_index(name='count')
agg_by_sex['percentage'] = 100 * (agg_by_sex['count'] / agg_by_sex['count'].sum())

# convert multidataframes to json
map_summaries = {'age_range': agg_by_age_range, 
                 'disappearance_year': agg_by_year, 
                 'tipology': agg_by_tipology, 
                 'category': agg_by_category, 
                 'sex': agg_by_sex
                 }
summaries = []
for k,v in map_summaries.items():
  row_summary = {}
  column = v.columns.to_list()[0]
  # fixes accents
  v[column] = v[column].apply(lambda x: unidecode.unidecode(x)) 
  row_summary['name'] = k
  # this is the key. to_json method return str so you have to reconvert to a list with json.loads. finally when you dump it doesn't display with "\"
  row_summary['data'] = json.loads(v.to_json(orient='records'))
  summaries.append(row_summary)

with open(OUTPUT, 'w') as f:
  json.dump(summaries, f)

print('JSON file created.')
# print('type(summaries): ', type(summaries))
# print('summaries: ', summaries)