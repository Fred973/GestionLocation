from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_ckeditor import CKEditor
from datetime import timedelta
from soft.constant import MYSQL_ALCHEMY, SCRET_KEY
from soft.src.config import Config, CKEditorConfig

# Create a Flask Instance
app = Flask(__name__)

# Database and project config
app.config.from_object(Config)
app.permanent_session_lifetime = timedelta(minutes=90)

# Initialize the databases
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Flask CKEditor
app.config.from_object(CKEditorConfig)
ckeditor = CKEditor(app)

# Cookie Session config
app.config['SESSION_COOKIE_SAMESITE'] = "Strict"

# Flask login stuff
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'not_logged_return'
login_manager.login_message = 'Vous devez être connecté pour accéder à la page'
login_manager.login_message_category = 'error'

""" Gestion Location """
# import mode.py to create tables
from soft.login import routes
from soft.gestion_loc import routes
from soft.gestion_loc.invoices import routes
from soft.gestion_loc.tenants import routes
from soft.gestion_loc.apartments import routes
from soft.gestion_loc.contracts import routes
from soft.gestion_loc.receipts import routes
from soft.database import routes

from soft.login import model
from soft.gestion_loc import model
from soft.gestion_loc.invoices import model
from soft.gestion_loc.tenants import model
from soft.gestion_loc.apartments import model
from soft.gestion_loc.contracts import model
from soft.gestion_loc.receipts import model
from soft.database import model

""" CCB11 Manager """
# import mode.py to create tables
from soft.ccb11_manager import routes

from soft.ccb11_manager import model

""" Experiences Manager """
from soft.experience import routes

from soft.experience import model

""" SAAB manager """
from soft.saab.questions import routes
from soft.saab import routes
from soft.saab.orders import routes
from soft.saab.tasks import routes

from soft.saab import model
from soft.saab.questions import model
from soft.saab.orders import model
from soft.saab.tasks import model
