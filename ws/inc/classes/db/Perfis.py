import json
import sys
import psycopg2
from psycopg2 import extras
import datetime
import jwt


sys.path.append('../../../')

from inc.consts.consts import Consts as consts
from inc.classes.lib.Db import DbLib
from inc.classes.lib.Password import Password
from inc.classes.db.Formacoes import DbFormacoes
from inc.classes.db.Paises import DbPaises

class DbPerfis:

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
        
    def c_perfil(self, input):
        
        data = {
            'ok': False,
            'errors': {},
            'data': {}
        }

        # Vars
        pas = Password()
        pai = DbPaises()
        fom = DbFormacoes()
        id_endereco = 0
        
        # Input
        perfil = ''
        username = ''
        nascimento = ''
        email = ''
        senha = ''
        id_pais = 0
        id_formacao = 0
        auth_token = ''


        # Params
        if input:
            if 'perfil' in input:
                perfil = str(input['perfil']['per_c_perfil']) if 'per_c_perfil' in input['perfil'] else ''
                username = str(input['perfil']['per_c_username']) if 'per_c_username' in input['perfil'] else ''                
                nascimento = str(input['perfil']['per_d_nascimento']) if 'per_d_nascimento' in input['perfil'] else ''    
                email = str(input['perfil']['per_c_email']) if 'per_c_email' in input['perfil'] else ''    
                senha = str(input['perfil']['per_c_senha']) if 'per_c_senha' in input['perfil'] else '' 
                id_pais = int(input['perfil']['per_fk_pais']) if 'per_fk_pais' in input['perfil'] else 0 
                id_formacao = int(input['perfil']['per_fk_formacao']) if 'per_fk_formacao' in input['perfil'] else 0 
        
        #     auth_token = str(input['authToken']) if 'authToken' in input else '' 
        # if auth_token:
        #     decoded = jwt.decode(auth_token, consts.JWT_SECRET, consts.JWT_ALGORITHM)
        #     if 'idPerfil' in decoded:
        #     else:
        #         data['errors']['401'] = '401'
        # else:
        #     data['errors']['401'] = '401'

        # Validation
        if not perfil:
            data['errors']['perfil'] = 'Perfil não indicado.'
        
        if not username:
            data['errors']['username'] = 'Username não indicado.'            
        else:
            username = username.strip()
            if len(username) > 40:
                data['errors']['username'] = 'Username deve ter menos que 40 caracteres.'
            else:
                resp = self.valor_em_campo('per_c_username', username)
                # data['resp'] = resp
                if resp:
                    if resp['ok']:
                        if resp['data']:
                            data['errors']['username'] = 'username já encontrado.'   
                    else:
                        data['errors']['username'] = 'Erro computando username.'    
                else:
                    data['errors']['username'] = 'Erro computando username.'
        
        if not email:
            data['errors']['email'] = 'Email não indicado.'
        else:
            resp = self.valor_em_campo('per_c_email', email)
            # data['resp'] = resp
            if resp:
                if resp['ok']:
                    if resp['data']:
                        data['errors']['email'] = 'Email já encontrado.'   
                else:
                    data['errors']['email'] = 'Erro computando email.'    
            else:
                data['errors']['email'] = 'Erro computando email.'

        if not senha:
            data['errors']['senha'] = 'Senha não indicada.'
        else:
            senha = pas.hash_password(senha)

        if id_pais < 1:
            data['errors']['pais'] = 'País não indicado.'
        else:
            resp = pai.r_pais(id_pais)
            if resp:
                if resp['ok']:
                    if not resp['data']:
                        data['errors']['pais'] = 'País inválido.'
                else:
                    data['errors']['pais'] = 'Erro lendo país.'
            else:
                data['errors']['pais'] = 'Erro lendo país.'
        
        if id_formacao > 0:
            resp = fom.r_formacao(id_formacao)
            # data['resp'] = resp
            if resp:
                if resp['ok']:
                    if not resp['data']:
                        data['errors']['formacao'] = 'Formação inválido.'
                else:
                    data['errors']['formacao'] = 'Erro lendo formação.'
            else:
                data['errors']['formacao'] = 'Erro lendo formação.'

        if not self.conn:
            data['errors']['conn'] = 'Erro de comunicação com o banco de dados.'

        if not data['errors']:
            try:
                cur = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
                dt_now = datetime.datetime.now()
                
                sql = """
                    INSERT INTO
                        perfis(
                            per_c_perfil,
                            per_c_username,
                            per_d_nascimento,
                            per_c_email,
                            per_c_senha,
                            per_fk_pais,
                            per_b_ativo,
                            per_fk_formacao,
                            per_dt_criado_em_serv
                        )VALUES (
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
                    perfil,
                    username,
                    nascimento,
                    email,
                    senha,
                    id_pais,
                    True,
                    id_formacao if id_formacao > 0 else None,
                    dt_now
                ]

                cur.execute(sql, bind)
                row = cur.fetchone()
                
                if not data['errors']:
                    data['ok'] = True
                    data['data'] = row['per_pk']
                    self.conn.commit()

            except (Exception, psycopg2.DatabaseError) as error:
                self.conn.rollback()
                data['errors']['conn'] = 'Erro na conexão com o banco de dados: ' + str(error)
            
            finally:
                if(cur):
                    cur.close()

        return data
    
    def r_login(self, credentials):
        
        data = {
            'ok': False,
            'errors': {},
            'data': {}
        }

        # Vars
        pas = Password()
        hash = ''
        auth_token = ''
        id_perfil = 0
        
        # Input
        username = ''
        password = ''

        # Params
        if credentials:
            username = str(credentials['username']) if 'username' in credentials else ''  
            password = str(credentials['password']) if 'password' in credentials else ''  
        
        # Validation
        if not username:
            data['errors']['username'] = 'Username não indicado.'
        
        if not password:
            data['errors']['password'] = 'Senha não indicado.'
        
        if not self.conn:
            data['errors']['conn'] = 'Erro de comunicação com o banco de dados.'

        if not data['errors']:
            try:
                cur = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

                sql = """
                    SELECT
                        per_pk,
                        per_c_senha
                    FROM
                        perfis
                    WHERE
                        per_c_username = %s
                """

                bind = [
                    username
                ]

                cur.execute(sql, bind)
                row = cur.fetchone()
                
                if row:
                    if 'per_c_senha' in row:
                        hash = row['per_c_senha']
                        if not pas.verify_password(hash, password):
                            data['errors']['login'] = 'Username/Senha incorretos.'                        
                    else:
                        data['errors']['login'] = 'Username/Senha não encontrados.'
                    
                    if 'per_pk' in row:
                        id_perfil = row['per_pk']
                    else:
                        data['errors']['login'] = 'Username/Senha não encontrados.'   
                else:
                    data['errors']['login'] = 'Username/Senha não encontrados.'

                if not data['errors']:
                    payload = {
                        'idPerfil' : str(id_perfil)
                    }

                    auth_token = jwt.encode(payload, consts.JWT_SECRET, consts.JWT_ALGORITHM)
                    auth_token = auth_token.decode('UTF-8')
                    # decoded = jwt.decode(auth_token, consts.JWT_SECRET, consts.JWT_ALGORITHM)
                    
                    data['ok'] = True
                    data['data'] = auth_token
                    self.conn.commit()

            except (Exception, psycopg2.DatabaseError) as error:
                self.conn.rollback()
                data['errors']['conn'] = 'Erro na conexão com o banco de dados: ' + str(error)
            
            finally:
                if(cur):
                    cur.close()

        return data

    def valor_em_campo(self, campo, valor, id=0):
    
        data = {
            'ok': False,
            'errors': {},
            'data': {}
        }

        # Vars

        # Validation
        if not campo:
            data['errors']['campo'] = 'Nenhum campo indicado.'
        
        if not valor:
            data['errors']['valor'] = 'Nenhum valor indicado.'

        if not data['errors']:
            try:
                cur = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
                
                sql = f"""
                    SELECT
                        *
                    FROM
                        perfis
                    WHERE
                        {campo} = '{valor}'
                        AND per_pk <> {id}
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
  