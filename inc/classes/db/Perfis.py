import json
import sys
import psycopg2
from psycopg2 import extras
import datetime

sys.path.append('../../../../')

from inc.consts.consts import Consts as consts
from inc.classes.lib.db import DbLib

class DbPerfis:

    def __init__(self, conn=None):
        if conn:
            self.conn = conn
        else:
            try:
                db = DbLib(sgbd='pgsql')
                conn = db.connect(db=consts.RECOMMENDIT_DB)
                conn.autocommit = False
                self.conn = conn
            except:
                self.conn = False
        
    def C_perfil(self, input):
        data = {
            'ok': False,
            'errors': {},
            'data': {}
        }

        # Vars

        # Input
        endereco = {}
        perfil = {}

        # Params
        endereco = input['endereco']
        perfil = input['perfil']        

        if not data['errors']:
            try:
                cur = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

                sql = f"""
                        INSERT INTO
                            enderecos(
                                end_c_cep,
                                end_c_logradouro,
                                end_i_numero,
                                end_c_localidade,
                                end_c_complemento,
                                end_c_bairro
                            )VALUES (
                                '{endereco['end_c_cep']}',
                                '{endereco['end_c_logradouro']}',
                                {endereco['end_i_numero']},
                                '{endereco['end_c_localidade']}',
                                '{endereco['end_c_complemento']}',
                                '{endereco['end_c_bairro']}'     
                            )
                            RETURNING *
                        ;
                        
                    """
                cur.execute(sql)
                id_endereco = cur.fetchone()['end_pk']

                if id_endereco < 1:
                    data['errors']['endereco'] = 'Erro criando endereço.'
                else:
                    sql = f"""
                        INSERT INTO
                            perfis(
                                per_c_perfil,
                                per_d_nascimento,
                                per_c_email,
                                per_c_senha,
                                per_fk_endereco,
                                per_dt_criado_em_serv
                            )VALUES (
                                '{perfil['per_c_perfil']}',
                                '{perfil['per_d_nascimento']}',
                                '{perfil['per_c_email']}',
                                '{perfil['per_c_senha']}',
                                {id_endereco},
                                '{datetime.datetime.now()}'    
                            )
                            RETURNING *
                        ;
                        
                    """
                    cur.execute(sql)
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


        # data['errors']['errorex'] = 'error1'      