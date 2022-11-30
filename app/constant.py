import os

# Constant configuration variable for Flask
user = 'root'
mdp = 'Fred973*'
mysql_sqalchemy = 'mysql+pymysql://{}:{}@localhost/gestion_loc'.format(user, mdp)
secret_key = "ma superbe cle secrete"
local_host = 'localhost'
db_name = 'gestion_loc'

# Variable for base direction
basedir = os.path.abspath(os.path.dirname(__file__))
