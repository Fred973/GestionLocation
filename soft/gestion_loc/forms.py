from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField
from wtforms.validators import DataRequired


# Create a Posts Form
class ApartmentForm(FlaskForm):
    """
    Apartment form structure:
        - apartment_name
        - address
        - zipcode
        - city
        - rent_price
        - submit
    """
    apartment_name = StringField("Alias", validators=[DataRequired()])
    address = StringField("Adresse", validators=[DataRequired()])
    zipcode = StringField("Code Postale", validators=[DataRequired()])
    city = StringField("Ville", validators=[DataRequired()])
    rent_price = FloatField("Montant de la location", validators=[DataRequired()])
    submit = SubmitField("Valider")


# Create a Posts Form
class ContractForm(FlaskForm):
    """
    Apartment form structure:
        - contract_nbr
        - file_name
        - submit
    """
    contract_nbr = StringField("N° de Contrat", validators=[DataRequired()])
    file_name = StringField("Contrat", validators=[DataRequired()])
    submit = SubmitField("Valider")