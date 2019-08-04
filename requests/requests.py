import sys

sys.path.append('../')
from inc.classes.db.Perfis import DbPerfis
from inc.consts.consts import Consts as consts

# C_perfil
C_perfil = {
    "perfil": {
        "per_c_perfil": "Mateus",
        "per_d_nascimento": "26/03/2001",
        "per_c_email": "mateuskb@icloud.com",
        "per_c_senha": "teste"
    },
    # "endereco": {
    #     "end_c_cep": "38017030",
    #     "end_c_logradouro": "Av. Odilon Fernandes",
    #     "end_i_numero": "235",
    #     "end_c_localidade": "Uberaba",
    #     "end_c_complemento": "Apto.1901",
    #     "end_c_bairro": "Estados Unidos"
    # }
}
per = DbPerfis()
print(per.C_perfil(C_perfil))
