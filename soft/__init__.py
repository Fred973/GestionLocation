from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from datetime import timedelta
from soft.constant import MYSQL_ALCHEMY, SCRET_KEY
from soft.src.config import Config

# Create a Flask Instance
app = Flask(__name__)

# Database and project config
app.config.from_object(Config)
app.permanent_session_lifetime = timedelta(hours=90)

# Initialize the databases
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Cookie Session config
app.config['SESSION_COOKIE_SAMESITE'] = "Strict"

# Flask login stuff
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Vous devez être connecté pour accéder à la page'
login_manager.login_message_category = 'error'

# import mode.py to create tables
from soft.login import routes
from soft.gestion_loc import routes
from soft.gestion_loc.invoices import routes
from soft.gestion_loc.tenants import routes
from soft.gestion_loc.apartments import routes
from soft.gestion_loc.contracts import routes
from soft.gestion_loc.receipts import routes
from soft.gestion_loc.database import routes

from soft.login import model
from soft.gestion_loc import model
from soft.gestion_loc.invoices import model
from soft.gestion_loc.tenants import model
from soft.gestion_loc.apartments import model
from soft.gestion_loc.contracts import model
from soft.gestion_loc.receipts import model
from soft.gestion_loc.database import model

