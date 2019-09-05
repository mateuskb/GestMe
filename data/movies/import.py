import pandas as pd
import ast, json
import datetime

# Vars
keywords = []
mov_word = {}
ratings = {}
collections = {} 
mov_col = {} # Add 1 to index
mov_gen = {} # Add 1 to index
genres = {}
movies = {} # Add 1 to index

# Imports
data_kw = pd.read_csv('keywords.csv', index_col='id')
data_rt = pd.read_csv('ratings_small.csv', index_col='movieId')
data_mv = pd.read_csv('movies_metadata.csv', low_memory=False)[:2]

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
data_mv = data_mv.set_index('id')

# Collections
collections = list(dict.fromkeys(data_mv['belongs_to_collection']))
# collections = ast.literal_eval(collections)

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

# ---- CLASS -----

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
    
    def get_collection_id(self, key):
        
        data = {
            'ok': False,
            'errors': {},
            'data': {}
        }

        key = str(key) if isinstance(key, int) else 0

        if key == 0:
            data['errors']['key'] = 'Chave não indicada.'
        
        if not data['errors']:
            if key in mov_col.keys():
                collection = mov_col[key]
                if collection:
                    if 'name' in collection.keys():
                        collection = collection['name']
                    else:
                        data['errors']['collection'] = 'Coleção inexistente.'
                else:
                    data['errors']['collection'] = 'Coleção inexistente.'
            else:
                data['errors']['key'] = 'Chave não existe.'

            if not data['errors']:
                try:
                    cur = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
                    
                    sql = """
                        SELECT
                            *
                        FROM
                            colecoes
                        WHERE
                            col_c_colecao = %s
                        ;
                    """
                    
                    bind = [
                        collection
                    ]

                    cur.execute(sql, bind)
                    row = cur.fetchone()
                    data['data'] = row['col_pk']
                
                    
                    data['ok'] = True
                    self.conn.commit()

                except (Exception, psycopg2.DatabaseError) as error:
                    self.conn.rollback()
                    data['errors']['conn'] = 'Erro na conexão com o banco de dados: ' + str(error)
                
                finally:
                    if(cur):
                        cur.close()

        return data
    
    def get_genres_id(self, key):
        
        data = {
            'ok': False,
            'errors': {},
            'data': {}
        }

        key = str(key) if isinstance(key, int) else 0

        if key == 0:
            data['errors']['key'] = 'Chave não indicada.'
        
        if not data['errors']:

            if key in mov_gen.keys():
                genres = mov_gen[key]
                if not genres:
                    data['errors']['key'] = 'Chave não existe.'
            else:
                data['errors']['key'] = 'Chave não existe.'

            if not data['errors']:
                ids_generos = []
                for gen in genres:
                    try:
                        cur = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
                        
                        sql = """
                            SELECT
                                *
                            FROM
                                categorias
                            WHERE
                                cat_c_categoria = %s
                            ;
                        """
                        
                        bind = [
                            gen
                        ]

                        cur.execute(sql, bind)
                        row = cur.fetchone()
                        ids_generos.append(row['cat_pk'])
                    
                        data['data'] = ids_generos
                        data['ok'] = True
                        self.conn.commit()

                    except (Exception, psycopg2.DatabaseError) as error:
                        self.conn.rollback()
                        data['errors']['conn'] = 'Erro na conexão com o banco de dados: ' + str(error)
                    
                    finally:
                        if(cur):
                            cur.close()

        return data
    
    def get_keywords_id(self, key):
        
        data = {
            'ok': False,
            'errors': {},
            'data': {}
        }

        key = key if isinstance(key, int) else 0

        if key == 0:
            data['errors']['key'] = 'Chave não indicada.'
        
        if not data['errors']:

            if key in mov_word.keys():
                keywords = mov_word[key]
                if not keywords:
                    data['errors']['key'] = 'Palavra não existe.'
            else:
                data['errors']['key'] = 'Chave não existe.'

            if not data['errors']:
                id_words = []
                for word in keywords:
                    try:
                        cur = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
                        
                        sql = """
                            SELECT
                                *
                            FROM
                                keywords
                            WHERE
                                key_c_keyword = %s
                            ;
                        """
                        
                        bind = [
                            word
                        ]

                        cur.execute(sql, bind)
                        row = cur.fetchone()
                        id_words.append(row['key_pk'])
                    
                        data['data'] = id_words
                        data['ok'] = True
                        self.conn.commit()

                    except (Exception, psycopg2.DatabaseError) as error:
                        self.conn.rollback()
                        data['errors']['conn'] = 'Erro na conexão com o banco de dados: ' + str(error)
                    
                    finally:
                        if(cur):
                            cur.close()

        return data


# ---- INSERTS -----


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

    def import_genres(self, genres):
        
        data = {
            'ok': False,
            'errors': {},
            'data': {}
        }

        genres_ids = []

        try:
            cur = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            
            for genre in genres:
                sql = """
                    INSERT INTO 
                        categorias(
                            cat_c_categoria
                        )VALUES(
                            %s
                        )
                        RETURNING *
                    ;
                """
                
                bind = [
                    genre
                ]

                cur.execute(sql, bind)
                row = cur.fetchone()
                genres_ids.append(row['cat_pk'])
        
            
            data['ok'] = True
            data['data'] = genres_ids
            self.conn.commit()

        except (Exception, psycopg2.DatabaseError) as error:
            self.conn.rollback()
            data['errors']['conn'] = 'Erro na conexão com o banco de dados: ' + str(error)
        
        finally:
            if(cur):
                cur.close()
        
        return data

    def import_collections(self, collections):
        
        data = {
            'ok': False,
            'errors': {},
            'data': {}
        }

        collections_ids = []
        cols = []
        a = 0
        try:
            cur = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            
            for col in collections:
                if isinstance(col, str):
                    col = ast.literal_eval(col)

                    if isinstance(col, dict):
                        name = col['name'] if col['name']  else ' '
                        poster_path = col['poster_path'] if col['poster_path'] else ' '

                        # if not name:
                        #     data['errors']['name'] = 'Erro name.'
                        # if not poster_path:
                        #     data['errors']['posterPath'] = poster_path

                        sql = """
                            INSERT INTO 
                                colecoes(
                                    col_c_colecao,
                                    col_c_image_path
                                )VALUES(
                                    %s,
                                    %s
                                )
                                RETURNING *
                            ;
                        """
                        
                        bind = [
                            name,
                            poster_path
                        ]

                        cur.execute(sql, bind)
                        row = cur.fetchone()
                        collections_ids.append(row['col_pk'])
                        # cols.append(col['name'])

            data['ok'] = True
            data['data'] = collections_ids
            self.conn.commit()

        except (Exception, psycopg2.DatabaseError) as error:
            self.conn.rollback()
            data['errors']['conn'] = 'Erro na conexão com o banco de dados: ' + str(error)
        
        finally:
            if(cur):
                cur.close()
        
        return data 

    def import_movies(self, movies):
        
        data = {
            'ok': False,
            'errors': {},
            'data': {}
        }

        try:
            cur = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            
            ids_cadastrados = []

            for key, info in movies.items():
                
                if info:
                    key = int(key)
                    adulto = bool(info['adult']) if 'adult' in info.keys() else False
                    homepage = info['homepage'] if 'homepage' in info.keys() else ''
                    title = info['original_title'] if 'original_title' in info.keys() else ''
                    descricao = info['overview'] if 'overview' in info.keys() else ''
                    popularidade = info['popularity'] if 'popularity' in info.keys() else ''
                    criado_em = info['release_date'] if 'release_date' in info.keys() else ''
                    conteudo = info['title'] if 'title' in info.keys() else ''
                    image_path = info['poster_path'] if 'poster_path' in info.keys() else ''
                    ratings_movie = ratings[key] if key in ratings.keys() else []

                    resp = self.get_collection_id(key)
                    if resp and not resp['errors']:
                        collection = resp['data']
                    else:
                        collection = None

                    resp = self.get_genres_id(key)
                    if resp and not resp['errors']:
                        genres = resp['data']
                    else:
                        genres = []

                    resp = self.get_keywords_id(key)
                    if resp and not resp['errors']:
                        keywords = resp['data']
                    else:
                        keywords = []

                    cadastrado_em = datetime.datetime.now()

                    sql = """
                        INSERT INTO 
                            conteudos(
                                con_c_conteudo,
                                con_t_descricao,
                                con_dt_cadastrado_em,
                                con_d_criado_em,
                                con_c_image_path,
                                con_b_adulto,
                                con_fk_colecao,
                                con_c_link,
                                con_c_titulo,
                                con_fk_tipo,
                                con_f_popularidade,
                                con_c_cod
                                )VALUES(
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s
                            )
                            RETURNING *
                        ;
                    """
                    
                    bind = [
                        conteudo,
                        descricao, 
                        cadastrado_em,
                        criado_em,
                        image_path,
                        adulto,
                        collection,
                        homepage,
                        title,
                        1,
                        popularidade,
                        key
                    ]

                    cur.execute(sql, bind)
                    row = cur.fetchone()
                    id_conteudo = row['con_pk']
                    ids_cadastrados.append(id_conteudo)

                    for gen in genres:
                        sql = """
                            INSERT INTO 
                                con_cat(
                                    cct_fk_categoria,
                                    cct_fk_conteudo
                                    )VALUES(
                                    %s,
                                    %s
                                )
                            ;
                        """
                        
                        bind = [
                            gen,
                            id_conteudo
                        ]

                        cur.execute(sql, bind)

                    for word in keywords:
                        sql = """
                            INSERT INTO 
                                con_key(
                                    ck_fk_keyword,
                                    ck_fk_conteudo
                                    )VALUES(
                                    %s,
                                    %s
                                )
                            ;
                        """
                        
                        bind = [
                            word,
                            id_conteudo
                        ]

                        cur.execute(sql, bind)
                    
                    for rat in ratings_movie:
                        sql = """
                            INSERT INTO 
                                ratings(
                                    rat_i_rating,
                                    rat_fk_conteudo
                                    )VALUES(
                                    %s,
                                    %s
                                )
                            ;
                        """
                        
                        bind = [
                            rat,
                            id_conteudo
                        ]

                        cur.execute(sql, bind)

            data['data'] = ids_cadastrados
            data['ok'] = True
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
# keywords_ids = resp['data']

# resp = cl.import_genres(genres) # DO NOT run it again
# genres_ids = resp['data']

# resp = cl.import_collections(collections) # DO NOT run it again
# collections_ids = resp['data']

# resp = cl.import_movies(movies) # DO NOT run it again

print(resp)
