from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class ReceiptForm(FlaskForm):
    """
    Receipt form structure:
        - first_name
        - name
        - phone
        - email
    """
    date_in = StringField("Date de Début", validators=[DataRequired()])
    date_out = StringField("Date de Fin", validators=[DataRequired()])
    submit = SubmitField("Valider")
