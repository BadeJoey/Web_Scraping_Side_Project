# -*- coding: utf-8 -*-
"""
Created on Tue Jul 27 21:10:11 2021

@author: Joey
"""

import pandas as pd

# Load our CSV from web_scrap.py
df = pd.read_csv("population_data_vancouver.csv")

# Drop old index
df.drop(columns=["Unnamed: 0"], inplace=True)
# Remove km2 and convert to float
df['area_of_postal_code'] = df['area_of_postal_code'].apply(lambda x: x.split(' ')[0]).astype('float')
# Remove ',' and convert to int
df['population'] = df['population'].apply(lambda x: x.replace(',', '')).astype('int')
# Convert to float
for column in ['median_age', 'male_median_age', 'female_median_age']:
    df[column] = df[column].apply(lambda x: x.split(' ')[0]).astype('float')

# Split the percentage and total number in 2 seperate columns each
for column in ['male_population', 'female_population']:
    # Split in two values
    series = df[column].apply(lambda x: x.split(' '))
    # Remove ',' and convert to int
    df[column] = series.apply(lambda x: x[0].replace(',', '')).astype('int')
    # If not 0 than split at '%' and afterwards at '('
    df[column + "_percentage"] = series.apply(lambda x: 
                                              x[1].split('%')[0].split('(')[1] 
                                              if x[0] != "0" 
                                              else 0).astype('float')

# Write the cleaned CSV
df.to_csv("population_data_vancouver_clean.csv")
