from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, TimeField, SubmitField, SelectField, DateField, IntegerField, BooleanField
from wtforms.validators import DataRequired
from wtforms.widgets import TextArea


class EquipmentListForm(FlaskForm):
    """
    EquipmentList form structure:
        - ata
        - description
        - part_number
        - alternate_pn
        - serial_number
        - batch
        - location
        - remarks
    """
    ata = IntegerField("ATA")
    description = StringField("Description", validators=[DataRequired()])
    part_number = StringField("Part Number", validators=[DataRequired()])
    alternate_pn = StringField("Alternate PN")
    serial_number = StringField("Serial Number")
    batch = StringField("Batch/Lot")
    location = StringField("Location")
    remarks = StringField("Remarks", widget=TextArea())
    submit = SubmitField("Save Equipment")

