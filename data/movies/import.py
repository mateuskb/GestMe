import pandas as pd
import psycopg2
import ast

# Vars
keywords = {}
collections = {}
mov_id = {}
movies = {}
ratings = {}

# Imports
data_kw = pd.read_csv('keywords.csv', index_col='id')
data_rt = pd.read_csv('ratings_small.csv', index_col='movieId')
# Data Handling
# Keywords
data_kw = data_kw.to_dict()['keywords']
for key, values in data_kw.items():
    values = ast.literal_eval(values)
    keywords[key] = []
    for item in values:
        keywords[key].append(item['name'])

# Ratings
data_rt = data_rt['rating']
for key, value in data_rt.items():
    if key in ratings.keys():
        ratings[key].append(value)
    else:
        ratings[key] = [value]


print(ratings)