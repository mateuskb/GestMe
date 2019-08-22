import json
import sys, os
import psycopg2
from psycopg2 import extras
import datetime
import jwt


BASE_PATH = os.path.abspath(__file__+ '/../../../../')
sys.path.append(BASE_PATH)

from inc.consts.consts import Consts as consts
from inc.classes.lib.Db import DbLib

class DbPaises:

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
        
    def r_pais(self, id_pais):

        data = {
            'ok': False,
            'errors': {},
            'data': {}
        }

        # Vars
        id_pais = int(id_pais) if id_pais else 0

        # Validation
        if id_pais < 1:
            data['errors']['idPais'] = 'Id de país não indicado.'
        
        if not self.conn:
            data['errors']['conn'] = 'Erro de comunicação com o banco de dados.'

        if not data['errors']:
            try:
                cur = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
                
                sql = """
                    SELECT
                        *
                    FROM
                        paises
                    WHERE
                        pai_pk = %s
                """
                
                bind = [
                    id_pais
                ]

                cur.execute(sql, bind)
                row = cur.fetchone()
                
                if not data['errors']:
                    data['ok'] = True
                    data['data'] = row
                    self.conn.commit()

            except (Exception, psycopg2.DatabaseError) as error:
                self.conn.rollback()
                data['errors']['conn'] = 'Erro na conexão com o banco de dados: ' + str(error)
            
            finally:
                if(cur):
                    cur.close()

        return data

    def r_paises(self):

        data = {
            'ok': False,
            'errors': {},
            'data': {}
        }

        # Validation
        if not self.conn:
            data['errors']['conn'] = 'Erro de comunicação com o banco de dados.'

        if not data['errors']:
            try:
                cur = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
                
                sql = """
                    SELECT
                        *
                    FROM
                        paises
                """

                cur.execute(sql)
                rows = cur.fetchall()
                
                if not data['errors']:
                    data['ok'] = True
                    data['data'] = rows
                    self.conn.commit()

            except (Exception, psycopg2.DatabaseError) as error:
                self.conn.rollback()
                data['errors']['conn'] = 'Erro na conexão com o banco de dados: ' + str(error)
            
            finally:
                if(cur):
                    cur.close()

        return data

    def r_pais_nome(self, input):

        data = {
            'ok': False,
            'errors': {},
            'data': {}
        }

        # Vars
        pais = ''
        
        # Params
        if input:
            pais = str(input['pai_c_pais']) if 'pai_c_pais' in input else ''

        # Validation
        if not pais:
            data['errors']['pais'] = 'País não indicado.'

        # Validation
        if not self.conn:
            data['errors']['conn'] = 'Erro de comunicação com o banco de dados.'

        if not data['errors']:
            try:
                cur = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
                
                sql = """
                    SELECT
                        *
                    FROM
                        paises
                    WHERE
                        pai_c_pais = %s
                    LIMIT 1
                    ;
                """

                bind = [
                    pais
                ]

                cur.execute(sql, bind)
                row = cur.fetchone()
                
                if not data['errors']:
                    data['ok'] = True
                    data['data'] = row
                    self.conn.commit()

            except (Exception, psycopg2.DatabaseError) as error:
                self.conn.rollback()
                data['errors']['conn'] = 'Erro na conexão com o banco de dados: ' + str(error)
            
            finally:
                if(cur):
                    cur.close()

        return data