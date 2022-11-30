from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from datetime import timedelta
from app.constant import mysql_sqalchemy, secret_key
from app.src.config import Config

# Create a Flask Instance
app = Flask(__name__)

# Database and project config
app.config.from_object(Config)
app.permanent_session_lifetime = timedelta(minutes=15)

# Initialize the database
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Flask login stuff
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Vous devez être connecté pour accéder à la page'
login_manager.login_message_category = 'error'

from app.login import routes
