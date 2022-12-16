from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class ContractForm(FlaskForm):
    """
    Contract form structure:
        - contract_nbr
        - file_name
        - submit
    """
    contract_nbr = StringField("N° de Contrat", validators=[DataRequired()])
    file_name = StringField("Contrat", validators=[DataRequired()])
    submit = SubmitField("Valider")
