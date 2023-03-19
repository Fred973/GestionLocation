from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired


# Create login form
class SAABLoginForm(FlaskForm):
    """
    Login form structure:
        - username
        - password
        - submit
    """
    username = StringField("User", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Log In")
