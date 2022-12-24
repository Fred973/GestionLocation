from wtforms import StringField, PasswordField, SubmitField, SelectField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired


# Create login form
class UserForm(FlaskForm):
    """
    User form structure:
        - username
        - password
        - submit
    """
    username = StringField("Utilisateur")
    category = SelectField("Catégorie (0=normal, 1=admin, 2=GestionLoc user)", choices=['0', '1', '2'], validators=[DataRequired()])
    password = PasswordField("Mot de passe")
    submit = SubmitField("Valider")
