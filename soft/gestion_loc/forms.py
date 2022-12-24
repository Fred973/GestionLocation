from wtforms import StringField, PasswordField, SubmitField
from flask_wtf import FlaskForm


# Create login form
class UserForm(FlaskForm):
    """
    User form structure:
        - username
        - password
        - submit
    """
    username = StringField("Utilisateur")
    category = StringField("Catégorie")
    password = PasswordField("Mot de passe")
    submit = SubmitField("Valider")
