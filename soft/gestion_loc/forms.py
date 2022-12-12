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
    Contract form structure:
        - contract_nbr
        - file_name
        - submit
    """
    contract_nbr = StringField("N° de Contrat", validators=[DataRequired()])
    file_name = StringField("Contrat", validators=[DataRequired()])
    submit = SubmitField("Valider")


# Create a Posts Form
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


# Create a Posts Form
class InvoiceForm(FlaskForm):
    """
    Invoice form structure:
        - invoice_number
        - description
        - added_date
        - file_name
    """
    invoice_number = StringField("N° de facture (si existant)", validators=[DataRequired()])
    description = StringField("Description", validators=[DataRequired()])
    added_date = StringField("Date", validators=[DataRequired()])
    file_name = StringField("Facture", validators=[DataRequired()])
    submit = SubmitField("Valider")