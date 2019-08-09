import sys
import requests
import base64
import json

sys.path.append('../../')
from request.environment import Environment

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
        resp = requests.request("POST", url, headers=headers)
        if resp.status_code == 200:
            resp = json.dumps(resp.text)
        else:
            resp = 'Unauthorized'
        return resp