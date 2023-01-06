from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DecimalField, SelectField, BooleanField
from wtforms.validators import DataRequired


class InvoiceInForm(FlaskForm):
    """
    Invoice In form structure:
        - invoice_number
        - description
        - added_date
        - file_name
    """

    who = SelectField("Qui", choices=['Georges', 'Katianne'], validators=[DataRequired()])
    aparts_name = SelectField("Appartement", choices=[], validators=[DataRequired()])
    invoice_number = StringField("N° de facture (si existant)")
    description = StringField("Description", validators=[DataRequired()])
    added_date = StringField("Date", validators=[DataRequired()])
    file_name = StringField("Facture")
    price = DecimalField("Somme", places=2, validators=[DataRequired()])
    tax_deductible = BooleanField("Déductible ? (oui si coché)")
    submit = SubmitField("Valider")


class InvoiceOutForm(FlaskForm):
    """
    Invoice Out form structure:
        - ref_customer
        - name
        - address
        - zipcode
        - city
        - phone
        - email
        - price
    """
    ref_customer = StringField("Référence Client")
    date_in = StringField("Date de début *")
    date_out = StringField("Date de fin *")
    due_date = StringField("Date d'échéance *")
    price = DecimalField("Prix (par jour) *", places=2, validators=[DataRequired()])

    submit = SubmitField("Valider")


class YearForm(FlaskForm):
    """
    year form structure:
        - year
    """
    year = SelectField("Choisir une année", choices=['2023', '2024', '2025', '2026', '2027', '2028', '2029', '2030'])

    submit = SubmitField("Changer")

