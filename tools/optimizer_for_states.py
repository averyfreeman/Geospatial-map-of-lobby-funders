#!/usr/bin/env .venv/bin/python3
import pandas as pd
import geopandas as gpd
""" 
this file:
    - loads the data csv file without the
    - columns we want, converts Year column
    - to_datetime() for time series calcs
    - creates ideas for possible subfiles
    - saves optimized file to disk
    - (this dataset was hassle-free compared to first one I tried)
"""

""" set options up here """
pd.set_option('display.max_rows', 200)
pd.options.display.float_format = '${:,.2f}'.format

dtypes = {
'Year': 'int',
'Employer_Name': 'string',
'Employer_City': 'string',
'Employer_State': 'string',
'Employer_Country': 'string',
'compensation': 'float',
'expenditures': 'float',
'agg_contrib': 'float',
'ballot_prop': 'float',
'entertain': 'float',
'vendor': 'float',
'expert_retain': 'float',
'inform_material': 'float',
'lobbying_comm': 'float',
'ie_in_support': 'float',
'itemized_exp': 'float',
'other_l3_exp': 'float',
'political': 'float',
'corr_compensation': 'float',
'corr_expend': 'float',
'total_exp': 'float',
'l3_nid': 'int',
'employer_nid': 'int'
}

# avoid cols 0, 3-5, & 8 (see usecols=lambda in read_csv)
omit = ['id', 'Employer_Email', 'Employer_Phone', 'Employer_Address', 'Employer_City', 'Employer_Zip', 'entertain', 'vendor', 'expert_retain', 'inform_material', 'ie_in_support', 'itemized_exp', 'other_l3_exp', 'corr_compensation', 'l3_nid']

df = pd.read_csv('Lobbyist_Employers_Summary_20240606.csv', usecols=lambda x: x not in omit, dtype=dtypes, parse_dates=['Year'])

shapefile = './us_states/cb_2018_us_state_500k.shp'
shape = gpd.read_file(shapefile)
print(df.info())

recast = {
'Year': 'category',
'employer_nid': 'int'
}

for col, type in recast.items():
    df[col] = df[col].astype(type)
    print(f'converted {col} to {type}')

# df.rename(columns={'Unnamed: 0':'position'}, inplace=True)
# to_rename = {
# 'Employer_Name': 'Funder',
# 'Employer_State': 'State',
# 'compensation': 'Lobby_Revenue',
# 'ballot': 'Ballot_Measures',
# 'political': 'Political_Contributions',
# }
# df = df.rename(columns=to_rename, inplace=True)

# print(df['Employer_State'])
print(shape['NAME'].to_string())

# df[df.select_dtypes('object').columns] = df.select_dtypes('object').fillna('')
# print('\nObject columns processed with na fills:')
# for column in df.select_dtypes('object'):
#     print(df[column].name)

# df[df.select_dtypes('float64').columns] = df.select_dtypes('float64').fillna(0)
# print('\nfloat64 columns processed with na fills:')
# for column in df.select_dtypes('float64'):
#     print(df[column].name)

# df[df.select_dtypes('int64').columns] = df.select_dtypes('int64').fillna(0)
# print('\nint64 columns processed with na fills:')
# for column in df.select_dtypes('int64'):
#     print(df[column].name)

# print(df.head())

# newdf = df.groupby('Employer_State')

# print(newdf)

# df['Year'] = df['Year'].apply(pd.to_datetime, unit='D')

# print('after basically all of the processing:')
# print(df.info())

# print('saving files with utf-8 encoding as optimized.csv and optimized.tsv')

# # saving .tsv, too, since easier to read
# df.to_csv('optimized.tsv', sep='\t', encoding='utf-8')
df.to_csv('states_year_over_year.csv', encoding='utf-8')

# print('please run main.py')