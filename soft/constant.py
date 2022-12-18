import os

# Constant configuration variable for Flask
DB_USER = 'root'
DB_PASSWORD = 'Fred973*'
MYSQL_ALCHEMY = 'mysql+pymysql://{}:{}@localhost/gestion_loc'.format(DB_USER, DB_PASSWORD)
SCRET_KEY = "9d7ac8ce47a5159ef96bd29f316cad4a"
DB_HOSTNAME = 'localhost'
DB_PORT = 3306
DB_NAME = 'gestion_loc'

# Variable for base direction
basedir = os.path.abspath(os.path.dirname(__file__))
rental_contracts_path = basedir + '/static/rental_contracts'
invoices_in_path = basedir + '/static/invoices/in'
invoices_out_path = basedir + '/static/invoices/out'
receipts_path = basedir + '/static/receipts'
db_save_path = basedir + '/db_save/'

# Various Data

george_json = {
    0: {
        'name': 'BAIA RIBEIRO',
        'first_name': 'Georges',
        'address': '3 rue EDGAR DEGAS ',
        'zipcode': '97310',
        'city': 'Kourou',
        'phone': '+594/694 97 20 39',
        'email': 'harison_baia@outlook.fr',
        'RIB': {
            'account_nbr': 'FR4620041010190035898Z01621',
            'BIC': 'PSSTFRPPCAY'
        }
    }
}

avio_json = {
    'id_customer': 0,
    'name': 'Société AVIO S.P.A.',
    'address': 'VIA LATINA SNC,(SP600 ARIANA KM5,2)',
    'zipcode': '00034',
    'city': 'COLLEFERRO (RM)'
}

receipt_text = "La présente quittance ne libère l'occupant que pour la période indiquée et annule tout reçu à valoir. Elle n'est pas libératoire des loyers ou indemnités d'occupation antérieurs impayés et est délivrée sous réserve de toutes instances judiciaires en cours."