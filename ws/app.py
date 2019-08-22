from flask import Flask, request, json
import sys
import base64

BASE_PATH = os.path.abspath(__file__+ './')
sys.path.append(BASE_PATH)

from inc.classes.lib.Request import RequestLib
from inc.classes.db.Perfis import DbPerfis
from inc.classes.db.Formacoes import DbFormacoes
from inc.classes.db.Paises import DbPaises

# App init
app = Flask(__name__)
app.config.update(
    TESTING=True,
    SECRET_KEY=b'_5#y2L"F4Q8z\n\xec]/'
)

# Classes
Perfis = DbPerfis()
Formacoes = DbFormacoes()
Paises = DbPaises()
Request_lib = RequestLib()

# App Routes
@app.route('/')
def index():
  return 'GestME index'

# PERFIS
@app.route('/login', methods=['POST'])
def login():
    resp = Request_lib.get_authorization(request, type='Basic', decode64=True)
    credentials = resp if resp else {}
    resp = Perfis.r_login(credentials)
    status = 200 if resp['ok'] else 401    
    response = app.response_class(
        response= json.dumps(resp),
        status=status,
        mimetype='application/json'
    )
    # return f'{credentials}'
    return response


@app.route('/perfis/add', methods=['POST'])
def c_perfil():
    input = request.json
    resp = Perfis.c_perfil(input)
    status = 200 if resp['ok'] else 401
    response = app.response_class(
        response= json.dumps(resp),
        status=status,
        mimetype='application/json'
    )
    return response

# PAISES
@app.route('/paises', methods=['GET'])
def r_paises():
    resp = Paises.r_paises()
    status = 200 if resp['ok'] else 404
    response = app.response_class(
        response= json.dumps(resp),
        status=status,
        mimetype='application/json'
    )
    return response

@app.route('/paises/nome', methods=['POST'])
def r_pais_nome():
    input = request.json
    resp = Paises.r_pais_nome(input)
    status = 200 if resp['ok'] else 401
    response = app.response_class(
        response= json.dumps(resp),
        status=status,
        mimetype='application/json'
    )
    return response

# FORMACOES
@app.route('/formacoes', methods=['GET'])
def r_formacoes():
    resp = Formacoes.r_formacoes()
    status = 200 if resp['ok'] else 404
    response = app.response_class(
        response= json.dumps(resp),
        status=status,
        mimetype='application/json'
    )
    return response
    
@app.route('/formacoes/nome', methods=['POST'])
def r_formacao_nome():
    input = request.json
    resp = Formacoes.r_formacao_nome(input)
    status = 200 if resp['ok'] else 401
    response = app.response_class(
        response= json.dumps(resp),
        status=status,
        mimetype='application/json'
    )
    return response


if __name__  == '__main__':
    app.run(debug=True)