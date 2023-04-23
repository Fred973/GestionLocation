from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, TimeField, SubmitField, SelectField, DateField, IntegerField, BooleanField
from wtforms.validators import DataRequired
from wtforms.widgets import TextArea

from soft.saab.tasks.model import JobCardList


class PartsListForm(FlaskForm):
    """
    EquipmentList form structure:
        - job_card
        - pn
        - sn
        - description
        - qty
        - reason
        - remarks
    """
    job_card = SelectField("Job Card N°", choices=[], validators=[DataRequired()])
    description = StringField("Description", validators=[DataRequired()])
    pn = StringField("Part Number", validators=[DataRequired()])
    sn = StringField("Serial Number")
    qty = IntegerField("Quantity", default=1, validators=[DataRequired()])
    reason = SelectField("Removed/Installed", choices=['Removed', 'Installed'], validators=[DataRequired()])
    remarks = StringField("Remarks", widget=TextArea())
    submit = SubmitField("Save Part")

    def __init__(self, *args, **kwargs):
        super(PartsListForm, self).__init__(*args, **kwargs)
        self.job_card.choices = [i.item_jc for i in JobCardList.query.all()]

