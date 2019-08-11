import json
import sys
import psycopg2
from psycopg2 import extras
import datetime
import jwt


sys.path.append('../../../')

from inc.consts.consts import Consts as consts
from inc.classes.lib.Db import DbLib

class DbFormacoes:

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
        
    def r_formacao(self, id_formacao):

        data = {
            'ok': False,
            'errors': {},
            'data': {}
        }

        # Vars
        id_formacao = int(id_formacao) if id_formacao else 0

        # Validation
        if id_formacao < 1:
            data['errors']['idFormacao'] = 'Id de formação não indicado.'
        
        if not self.conn:
            data['errors']['conn'] = 'Erro de comunicação com o banco de dados.'

        if not data['errors']:
            try:
                cur = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
                
                sql = """
                    SELECT
                        *
                    FROM
                        formacoes
                    WHERE
                        for_pk = %s
                """
                
                bind = [
                    id_formacao
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

    def r_formacoes(self):

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
                        formacoes
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