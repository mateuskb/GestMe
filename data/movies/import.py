import pandas as pd
import psycopg2
import ast, json

# Vars
keywords = []
mov_word = {}
ratings = {}
collections = {} 
mov_col = {} # Add 1 to index
mov_id = {} # Add 1 to index
genres = {}
movies = {} # Add 1 to index

# Imports
data_kw = pd.read_csv('keywords.csv', index_col='id')
data_rt = pd.read_csv('ratings_small.csv', index_col='movieId')
data_mv = pd.read_csv('movies_metadata.csv', low_memory=False)[:50]

# --- Data Handling ---

# Keywords
a = []
keywords = list(dict.fromkeys(data_kw['keywords']))

for keyword_list in keywords:
    keyword_list = ast.literal_eval(keyword_list)
    for word in keyword_list:
        a.append(word['name'])

keywords = a

data_kw = data_kw.to_dict()['keywords']

for key, values in data_kw.items():
    values = ast.literal_eval(values)
    mov_word[key] = []
    for item in values:
        mov_word[key].append(item['name'])

# Ratings
data_rt = data_rt['rating']
for key, value in data_rt.items():
    if key in ratings.keys():
        ratings[key].append(value)
    else:
        ratings[key] = [value]

# Movies
mov_id = data_mv['id']
data_mv = data_mv.set_index('id')

# Collections
# a = []
# collections = list(dict.fromkeys(data_mv['belongs_to_collection']))

# for col in collections:
#     for c in col:
#         # c = ast.literal_eval(c)
#         a.append(c)

# collections = a

col = data_mv['belongs_to_collection']
for key, value in col.items():
    mov_col[key] = {}

    if isinstance(value, str): # Belong to a collection
        value = ast.literal_eval(value)
        mov_col[key]['name'] = value['name']
        mov_col[key]['poster_path'] = value['poster_path']
    else:
        mov_col[key] = None
    
# Genres
# gen = data_mv['genres']
# for key, value in col.items():
#     collections[key] = {}

#     if isinstance(value, str): # Belong to a collection
#         value = ast.literal_eval(value)
#         collections[key]['name'] = value['name']
#         collections[key]['poster_path'] = value['poster_path']
#     else:
#         collections[key] = None

print(a)

