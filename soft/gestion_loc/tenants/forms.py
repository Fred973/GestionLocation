from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class TenantForm(FlaskForm):
    """
    Tenant form structure:
        - first_name
        - name
        - phone
        - email
    """
    first_name = StringField("Prénom", validators=[DataRequired()])
    name = StringField("Nom", validators=[DataRequired()])
    phone = StringField("Téléphone", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    submit = SubmitField("Valider")
