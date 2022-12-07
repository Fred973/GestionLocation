from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired
from flask_wtf import FlaskForm


# Create login form
class LoginForm(FlaskForm):
    """
    Login form structure:
        - username
        - password
        - submit
    """
    username = StringField("Utilisateur", validators=[DataRequired()])
    password = PasswordField("Mot de passe", validators=[DataRequired()])
    submit = SubmitField("Se connecter")
