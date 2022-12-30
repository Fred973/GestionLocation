from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SelectField, DateField, SubmitField
from wtforms.validators import DataRequired
from wtforms.widgets import TextArea
import csv
from soft.constant import utils_path

ata = []
with open(r'{}{}'.format(utils_path, 'ata.csv')) as file:
    csvreader = csv.reader(file)
    for i in csvreader:
        ata.append(i)


class TechLogForm(FlaskForm):
    """
    - date
    - ac_type
    - registration
    - ata
    - work_order
    - description
    - work_type
    - time
    - function
    """
    date = DateField("Date", validators=[DataRequired()])
    ac_type = StringField("A/C Type", validators=[DataRequired()])
    registration = StringField("Registration", validators=[DataRequired()])
    ata = SelectField("ATA", choices=ata, validators=[DataRequired()])
    work_order = StringField("Work Order", validators=[DataRequired()])
    description = StringField("Description", widget=TextArea(), validators=[DataRequired()])

    work_type = SelectField(
        "Work Type",
        choices=['Inspection', 'Maintenance', 'Remove/Install', 'Troubleshooting', 'Functional Test'],
        validators=[DataRequired()]
    )

    time = FloatField("Time", validators=[DataRequired()])

    function = SelectField(
        "Function",
        choices=['Support', 'RTS EASA', 'RTS FAA'],
        validators=[DataRequired()]
    )
    submit = SubmitField("Validate")
