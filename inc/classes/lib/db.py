import sys
import psycopg2
from psycopg2 import extras

sys.path.insert(1, './../../consts')

from consts import Consts as consts

class DbLib:

    def __init__(self, sgbd='pgsql'):
        self.sgbd = sgbd
    
    # def connect(db):

print(consts.SGBDS)