import sys
import psycopg2
from psycopg2 import extras

sys.path.append('../../../')
from inc.consts.consts import Consts as consts

class DbLib:

    def __init__(self, sgbd='pgsql'):
        if sgbd in consts.SGBDS:
            self.sgbd = sgbd
        else:
            self.sgbd = ''
    
    def connect(self, db=consts.RECOMMENDIT_DB):
        if self.sgbd == 'pgsql':
            try:
                conn = psycopg2.connect(host=db['hostname'], user=db['username'], password=db['password'], dbname=db['database'])
                return conn
            except:
                return False
        else:
            return False


# try:
#     db = DbLib(sgbd='pgsql')
#     _conn = db.connect(db=consts.RECOMMENDIT_DB)
#     _conn.autocommit = False
#     if _conn == False:
#         print('Erro de conexão com o banco de dados.')

#     cur = _conn.cursor(cursor_factory=extras.RealDictCursor)
#     try:
#         cur.execute("""SELECT * from enderecos""")
#     except:
#         print("I can't SELECT from bar")
#     rows = cur.fetchall()
#     print(len(rows))
#     _conn.commit()
#     print("Transaction completed successfully ")

# except (Exception, psycopg2.DatabaseError) as error:
#     _conn.rollback()
#     print ("Error in transction Reverting all other operations of a transction ", error)

# finally:
#     if(_conn):
#         cur.close()
#         _conn.close()
#         print("PostgreSQL connection is closed")