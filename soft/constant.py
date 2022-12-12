import os

# Constant configuration variable for Flask
user = 'root'
mdp = 'Fred973*'
mysql_sqalchemy = 'mysql+pymysql://{}:{}@localhost/gestion_loc'.format(user, mdp)
secret_key = "9d7ac8ce47a5159ef96bd29f316cad4a"
local_host = 'localhost'
db_name = 'gestion_loc'

# Variable for base direction
basedir = os.path.abspath(os.path.dirname(__file__))
rental_contracts_path = basedir + '/static/rental_contracts'
invoices_path = basedir + '/static/invoices'