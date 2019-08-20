import sys, os
import requests
import base64
import json

BASE_PATH = os.path.abspath(__file__+ '/../../')

sys.path.append(BASE_PATH)
from inc.environment import Environment

class Requests:

    # Perfis
    @staticmethod
    def login(username, password):
        input = {
            "username": username.strip(),
            "password": password.strip()
        }
        input = base64.b64encode(json.dumps(input).encode()).decode()
        
        url = Environment.REQUEST_URL + '/login'
        headers = {
            'Authorization': f"Basic {input}"
        }
        try:
            resp = requests.request("POST", url, headers=headers)
            status = resp.status_code
            resp = resp.json()
            resp['status'] = status
        except:
            resp = False
        return resp
        
    @staticmethod
    def c_perfil(name, username, email, password, birthday, id_pais, id_formacao):
        input = {
            "perfil": {
                "per_c_perfil": name,
                "per_c_username": username,
                "per_d_nascimento": birthday,
                "per_c_email": email,
                "per_c_senha": password,
                "per_fk_pais": id_pais,
                "per_fk_formacao": id_formacao
            }
        }
        
        url = Environment.REQUEST_URL + '/perfis/add'

        try:
            resp = requests.request("POST", url, json=input)
            status = resp.status_code
            resp = resp.json()
            resp['status'] = status
        except:
            resp = False
        return resp

    # Formações
    @staticmethod
    def r_formacoes():
        url = Environment.REQUEST_URL + '/formacoes'
        try:
            resp = requests.request("GET", url)
            status = resp.status_code
            resp = resp.json()
            resp['status'] = status
        except:
            resp = False
        return resp

    @staticmethod
    def r_formacao_nome(formacao):
        url = Environment.REQUEST_URL + '/formacoes/nome'
        input = {'for_c_formacao': formacao}
        try:
            resp = requests.request("POST", url, json=input)
            status = resp.status_code
            resp = resp.json()
            resp['status'] = status
        except:
            resp = False
        return resp
    
    # Países
    @staticmethod
    def r_paises():
        url = Environment.REQUEST_URL + '/paises'
        try:
            resp = requests.request("GET", url)
            status = resp.status_code
            resp = resp.json()
            resp['status'] = status
        except:
            resp = False
        return resp
    
    @staticmethod
    def r_pais_nome(pais):
        url = Environment.REQUEST_URL + '/paises/nome'
        input = {'pai_c_pais': pais}
        try:
            resp = requests.request("POST", url, json=input)
            status = resp.status_code
            resp = resp.json()
            resp['status'] = status
        except:
            resp = False
        return resp