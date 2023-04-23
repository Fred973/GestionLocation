from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, TimeField, SubmitField, SelectField, DateField, IntegerField, BooleanField
from wtforms.validators import DataRequired
from wtforms.widgets import TextArea


class JobCardListForm(FlaskForm):
    """
    TasksList form structure:
        - item_jc
        - description
        - remarks
    """
    item_jc = IntegerField("Job card Number (Work Order)")
    description = StringField("Description")
    remarks = StringField("Remarks", widget=TextArea())
    submit = SubmitField("Save Job card")


class JobCardDetailsForm(FlaskForm):
    """
    TasksList form structure:
        - job_card
        - type
        - mm_ref
        - description
        - remarks
        - working_time
        - nbr_tech
        - performed
    """
    job_card = StringField("Job card Number (SAAB)")
    type = SelectField("Type", choices=["Lubrication", "Inspection", "Operational Check", "Functional Check", "Troubleshooting", "Servicing", "Removal / Installation", "Replacement", "Corrosion Prevention"], validators=[DataRequired()])
    mm_ref = StringField("Maintenance Manual reference")
    description = StringField("Description")
    reason = SelectField("Parts Removed/Installed details", choices=['Removed', 'Installed'])
    remarks = StringField("Remarks", widget=TextArea())
    working_time = TimeField("Working Time")
    nbr_tech = IntegerField("Number of Technicians needed")
    performed = BooleanField("Performed ?")
    submit = SubmitField("Save Task")
