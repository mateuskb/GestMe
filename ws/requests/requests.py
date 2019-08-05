import sys

sys.path.append('../')
from inc.classes.db.Perfis import DbPerfis
from inc.consts.consts import Consts as consts

# Peris
c_perfil = {
    "perfil": {
        "per_c_perfil": "Ana Laura Nakamura",
        "per_c_username": "a_nakamura",
        "per_d_nascimento": "31/07/2000",
        "per_c_email": "teste@gmail.com",
        "per_c_senha": "testes"
    }
}

r_login = {
    "username": "mateuskb",
    "password": "teste"
}


per = DbPerfis()
# print(per.c_perfil(c_perfil))
print(per.r_login(r_login))