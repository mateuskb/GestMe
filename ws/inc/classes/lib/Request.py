import sys, os
import psycopg2
from psycopg2 import extras
import base64
import json

BASE_PATH = os.path.abspath(__file__+ '/../../../../')
sys.path.append(BASE_PATH)

from inc.consts.consts import Consts as consts

class RequestLib:

    def __init__(self):
        pass
    
    def get_authorization(self, request, type='Bearer', decode64=False):
        type = type if type in consts.AUTHORIZATION_TYPE else ''
        if not type:
            return False
        else:
            try:
                credentials = request.headers.get('Authorization').strip(type + ' ')
                if decode64:
                    credentials = base64.b64decode(credentials.encode())
                    credentials = json.loads(credentials)
                return credentials
            except:
                return False
