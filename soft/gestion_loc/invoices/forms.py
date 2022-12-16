from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DecimalField
from wtforms.validators import DataRequired


class InvoiceInForm(FlaskForm):
    """
    Invoice In form structure:
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
    first_name = StringField("Prénom")
    name = StringField("Nom *", validators=[DataRequired()])
    address = StringField("Adresse *", validators=[DataRequired()])
    zipcode = StringField("Code Postale *", validators=[DataRequired()])
    city = StringField("Ville *", validators=[DataRequired()])
    phone = StringField("Téléphone")
    email = StringField("Email")
    month = StringField("Mois")
    date_in = StringField("Date de début *")
    date_out = StringField("Date de fin *")
    due_date = StringField("Date d'échéance")
    price = DecimalField("Prix (jour/mois) *",places=2, validators=[DataRequired()])

    submit = SubmitField("Valider")
