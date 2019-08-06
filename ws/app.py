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
  
@app.route('/login', methods=['POST'])
def login():
    credentials = {}
    status = 401

    try:    
        credentials = request.json
    except:
        status = 401

    resp = Perfis.r_login(credentials)
    if resp:
        if resp['ok']:
            status=200
        else:
            status=401

    response = app.response_class(
        response= json.dumps(resp),
        status=status,
        mimetype='application/json'
    )

    return response
 
if __name__  == '__main__':
    app.run(debug=True)