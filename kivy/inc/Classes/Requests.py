import sys
import requests
import base64
import json

sys.path.append('../../')
from inc.environment import Environment

class Requests:
    
    # def __init__(self):
    #     pass
    
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
    
    