from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SubmitField, SelectField
from wtforms.validators import DataRequired


class ApartmentForm(FlaskForm):
    """
    Apartment form structure:
        - apartment_name
        - address
        - zipcode
        - city
        - rent_price
        - month_day
        - submit
    """
    apartment_name = StringField("Alias", validators=[DataRequired()])
    address = StringField("Adresse", validators=[DataRequired()])
    zipcode = StringField("Code Postale", validators=[DataRequired()])
    city = StringField("Ville", validators=[DataRequired()])
    rent_price = FloatField("Montant de la location", validators=[DataRequired()])
    month_day = SelectField("Mode de Paiement (Jour/Mois) ", choices=['Par Mois', 'Par Jour'], validators=[DataRequired()])
    submit = SubmitField("Valider")
