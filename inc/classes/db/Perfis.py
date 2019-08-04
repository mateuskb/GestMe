import json
import sys
import psycopg2
from psycopg2 import extras
from psycopg2 import sql
import datetime

sys.path.append('../../../')

from inc.consts.consts import Consts as consts
from inc.classes.lib.db import DbLib
from inc.classes.lib.password import Password

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
        pas = Password()
        id_endereco = 0
        
        # Input
        perfil = ''
        nascimento = ''
        email = ''
        senha = ''
        cep = ''
        localidade = ''
        logradouro = ''
        numero = 0
        complemento = ''
        bairro = ''


        # Params
        if input:
            if 'perfil' in input:
                perfil = str(input['perfil']['per_c_perfil']) if 'per_c_perfil' in input['perfil'] else ''
                nascimento = str(input['perfil']['per_d_nascimento']) if 'per_d_nascimento' in input['perfil'] else ''    
                email = str(input['perfil']['per_c_email']) if 'per_c_email' in input['perfil'] else ''    
                senha = str(input['perfil']['per_c_senha']) if 'per_c_senha' in input['perfil'] else ''    
            if 'endereco' in input:
                cep = str(input['endereco']['end_c_cep']) if 'end_c_cep' in input['endereco'] else ''
                logradouro = str(input['endereco']['end_c_logradouro']) if 'end_c_logradouro' in input['endereco'] else ''    
                localidade = str(input['endereco']['end_c_localidade']) if 'end_c_localidade' in input['endereco'] else ''    
                complemento = str(input['endereco']['end_c_complemento']) if 'end_c_complemento' in  input['endereco'] else ''  
                bairro = str(input['endereco']['end_c_bairro']) if 'end_c_bairro' in input['endereco'] else ''  
                numero = int(input['endereco']['end_i_numero']) if 'end_i_numero' in input['endereco'] else 0 

        # Validation
        if not perfil:
            data['errors']['perfil'] = 'Perfil não indicado.'
        else:
            pass 
        
        if not email:
            data['errors']['email'] = 'Email não indicado.'
        else:
            pass 

        if not senha:
            data['errors']['senha'] = 'Senha não indicada.'
        else:
            senha = pas.hash_password(senha)

        if 'endereco' in input:
            if not cep:
                data['errors']['cep'] = 'Cep não indicado.'
            if not logradouro:
                data['errors']['logradouro'] = 'Logradouro não indicado.'
            if not localidade:
                data['errors']['localidade'] = 'Localidade não indicada.'
            if not bairro:
                data['errors']['bairro'] = 'Bairro não indicado.'
            if numero < 1:
                data['errors']['numero'] = 'Número inválido.'


        if not data['errors']:
            try:
                cur = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

                if 'endereco' in input:
                    sql = """
                            INSERT INTO
                                enderecos(
                                    end_c_cep,
                                    end_c_logradouro,
                                    end_i_numero,
                                    end_c_localidade,
                                    end_c_complemento,
                                    end_c_bairro
                                )VALUES (
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
                        cep,
                        logradouro,
                        str(numero),
                        localidade,
                        complemento,
                        bairro
                    ]

                    cur.execute(sql, bind)
                    id_endereco = cur.fetchone()['end_pk']

                    if id_endereco < 1:
                        data['errors']['endereco'] = 'Erro criando endereço.'

                dt_now = datetime.datetime.now()
                
                sql = """
                    INSERT INTO
                        perfis(
                            per_c_perfil,
                            per_d_nascimento,
                            per_c_email,
                            per_c_senha,
                            per_fk_endereco,
                            per_dt_criado_em_serv
                        )VALUES (
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
                    perfil,
                    nascimento,
                    email,
                    senha,
                    str(id_endereco) if id_endereco > 0 else None,
                    dt_now
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


        # data['errors']['errorex'] = 'error1'      