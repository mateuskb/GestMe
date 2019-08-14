import sys
import requests
import base64
import json
from kivy.storage.jsonstore import JsonStore

sys.path.append('../../')
from inc.environment import Environment
from inc.consts.consts import Consts

class Storage:

    @staticmethod
    def logoff():
        resp = False
        try:
            storage = JsonStore("../../" + Consts.JSON_PATH)
            storage.delete('login')
            resp = True
        except:
            resp = False
        return resp
    
    @staticmethod
    def r_authtoken():
        resp = False
        try:
            storage = JsonStore("../../" + Consts.JSON_PATH)
            resp = storage['login']
        except:
            resp = False
        return resp

# resp = Storage.r_authtoken()
# print(resp)