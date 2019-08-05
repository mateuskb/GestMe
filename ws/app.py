from flask import Flask, request, json
import sys
app = Flask(__name__)

sys.path.append('./')
from inc.classes.db.Perfis import DbPerfis

# Classes
Perfis = DbPerfis()

# App Routes
@app.route('/')
def index():
  return 'This is RECOMMENDIT API index'
  
PREFIX = '/perfis'
@app.route(PREFIX + '/login', methods=['POST'])
def login():
    credentials = {}
    try:
        credentials = request.json
        if request.method == 'POST':
            response = app.response_class(
                response= json.dumps(Perfis.r_login(credentials)),
                status=200,
                mimetype='application/json'
            )
    except:
        response = app.response_class(
                response= json.dumps(Perfis.r_login(credentials)),
                status=401,
                mimetype='application/json'
            )
    return response 