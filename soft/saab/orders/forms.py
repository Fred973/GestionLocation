from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SubmitField, SelectField, DateField, IntegerField
from wtforms.validators import DataRequired
from wtforms.widgets import TextArea


class OrderListForm(FlaskForm):
    """
    OrderList form structure:
        - part_number
        - description
        - qty
        - job_card
        - remark
        - order_sent_on
        - received_on
    """
    part_number = StringField("Part Number", validators=[DataRequired()])
    description = StringField("Description", validators=[DataRequired()])
    qty = StringField("Quantity", validators=[DataRequired()])
    job_card = IntegerField("Job Card N°", validators=[DataRequired()])
    remark = StringField("Remarks", widget=TextArea())
    order_sent_on = DateField("Order sent on", )
    submit = SubmitField("Save order")
