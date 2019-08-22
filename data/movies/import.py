import pandas as pd
import ast, json

# Vars
keywords = []
mov_word = {}
ratings = {}
collections = {} 
mov_col = {} # Add 1 to index
mov_id = {} # Add 1 to index
mov_gen = {} # Add 1 to index
genres = {}
movies = {} # Add 1 to index

# Imports
data_kw = pd.read_csv('keywords.csv', index_col='id')
data_rt = pd.read_csv('ratings_small.csv', index_col='movieId')
data_mv = pd.read_csv('movies_metadata.csv', low_memory=False)[:15]

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
collections = list(dict.fromkeys(data_mv['belongs_to_collection']))

col = data_mv['belongs_to_collection']
for key, value in col.items():
    mov_col[key] = {}

    if isinstance(value, str): # Belong to a collection
        value = ast.literal_eval(value)
        if isinstance(value, dict):
            mov_col[key]['name'] = value['name']
            mov_col[key]['poster_path'] = value['poster_path']
        else:
            mov_col[key] = None
    else:
        mov_col[key] = None
    
# Genres
a = []
genres = list(dict.fromkeys(data_mv['genres']))

for genres_list in genres:
    genres_list = ast.literal_eval(genres_list)
    for word in genres_list:
        a.append(word['name'])

genres = list(dict.fromkeys(a))

gen = data_mv['genres']
for key, values in gen.items():
    values = ast.literal_eval(values)
    mov_gen[key] = []
    for item in values:
        mov_gen[key].append(item['name'])

# Movies
movies = data_mv.drop(['belongs_to_collection', 'budget', 'genres', 'imdb_id', 'original_language',
                       'production_companies', 'production_countries', 'revenue', 'runtime', 'spoken_languages',
                       'status', 'tagline', 'video', 'vote_average', 'vote_count'], axis=1)

movies = movies.T.to_dict()


# ---- INSERTS -----

keywords_ids = []

import sys, os
import psycopg2
from psycopg2 import extras

BASE_PATH = os.path.abspath(__file__+ '/../../../')
sys.path.append(BASE_PATH)

from ws.inc.classes.lib.Db import DbLib
from ws.inc.consts.consts import Consts as consts

class DbImports:

    def __init__(self, conn=None):
        if conn:
            self.conn = conn
        else:
            try:
                db = DbLib(sgbd='pgsql')
                conn = db.connect(db=consts.GESTME_DB)
                conn.autocommit = False
                self.conn = conn
            except:
                self.conn = False
    
    def import_keywords(self, keywords):
        
        data = {
            'ok': False,
            'errors': {},
            'data': {}
        }

        keywords_ids = []

        try:
            cur = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            
            for word in keywords:
                sql = """
                    INSERT INTO 
                        keywords(
                            key_c_keyword
                        )VALUES(
                            %s
                        )
                        RETURNING *
                    ;
                """
                
                bind = [
                    word
                ]

                cur.execute(sql, bind)
                row = cur.fetchone()
                keywords_ids.append(row['key_pk'])
        
            
            data['ok'] = True
            data['data'] = keywords_ids
            self.conn.commit()

        except (Exception, psycopg2.DatabaseError) as error:
            self.conn.rollback()
            data['errors']['conn'] = 'Erro na conexão com o banco de dados: ' + str(error)
        
        finally:
            if(cur):
                cur.close()
        
        return data


# Run imports
cl = DbImports()

# resp = cl.import_keywords(keywords) # DO NOT run it again

# print(resp['data'])