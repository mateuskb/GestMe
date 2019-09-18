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

class DbConteudos:

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
        
    def r_conteudo_id(self, input):

        data = {
            'ok': False,
            'errors': {},
            'data': {}
        }
        # data['input'] = input

        # Vars
        id_conteudo = 0
        auth_token = ''

        # Params
        if input:
            id_conteudo = int(input['idConteudo']) if 'idConteudo' in input else ''
            auth_token = str(input['authToken']) if 'authToken' in input else ''

        # data['idConteudo'] = id_conteudo
        # data['authToken'] = auth_token

        # Validation
        if not auth_token:
            data['errors']['401'] = 'Token não indicado.'
        else:
            try:
                payload_auth = jwt.decode(auth_token, key=consts.JWT_SECRET, algorithms=[consts.JWT_ALGORITHM])
            except Exception as error:
                data['errors']['401'] = str(error)

        if id_conteudo < 1:
            data['errors']['idConteudo'] = 'Conteúdo não indicado.'

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
                        conteudos
                    WHERE
                        con_pk = %s
                    LIMIT 1
                    ;
                """

                bind = [
                    id_conteudo
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
