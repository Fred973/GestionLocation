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

    aparts_name = SelectField("Appartement", choices=[], validators=[DataRequired()])
    ref_invoice = StringField("N° de facture (si existant)")
    description = StringField("Description", validators=[DataRequired()])
    added_date = StringField("Date", validators=[DataRequired()])
    file_name = StringField("Facture")
    price = DecimalField("Somme", places=2, validators=[DataRequired()])
    tax_deductible = BooleanField("Déductible ? (oui si coché)")
    common_invoice = BooleanField("Facture commune ? (Uniquement pour le 7 !)")
    submit = SubmitField("Valider")


class InvoiceOutForm(FlaskForm):
    """
    Invoice Out form structure:
        - apartment_name
        - ref_customer
        - date_in
        - date_out
        - due_date
        - price
    """
    apartment_name = SelectField("Appartement", choices=[], validators=[DataRequired()])
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


class AllInvoicesOutForm(FlaskForm):
    """
    All invoices out structure
        - validate
    """
    submit = SubmitField("Télécharger")


class DateSelectForm(FlaskForm):
    """
    All invoices out structure
        - validate
    """
    month_list = SelectField("Choisir le mois", choices=[])
    submit = SubmitField("Changer")