from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from datetime import timedelta
from soft.constant import mysql_sqalchemy, secret_key
from soft.src.config import Config

# Create a Flask Instance
app = Flask(__name__)

# Database and project config
app.config.from_object(Config)
app.permanent_session_lifetime = timedelta(hours=90)

# Initialize the database
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Flask login stuff
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'index'
login_manager.login_message = 'Vous devez être connecté pour accéder à la page'
login_manager.login_message_category = 'error'

# import mode.py to create tables
from soft.login import routes
from soft.gestion_loc import routes
from soft.login import model
from soft.gestion_loc import model

