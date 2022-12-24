from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SubmitField, SelectField, DateField
from wtforms.validators import DataRequired
from wtforms.widgets import TextArea

from soft.func.db_func import get_table_list


class TaskForm(FlaskForm):
    """
    Task form structure:
        - type
        - description
        - added_date
        - relevance
        - closed_date
        - remarks
        - status
    """
    type = SelectField("Task Type",
                       choices=['Admin', 'Various', 'Shipping', 'Cleaning', 'Stock', 'Tools', 'Maintenance'],
                       validators=[DataRequired()]
                       )
    description = StringField("Description", validators=[DataRequired()], widget=TextArea())
    added_date = DateField("Creation Date", validators=[DataRequired()])
    relevance = SelectField("Relevance",
                            choices=['Major', 'Minor'],
                            validators=[DataRequired()]
                            )
    closed_date = DateField("Closure Date", )
    remarks = StringField("Remarks", widget=TextArea())
    status = SelectField("Status", choices=['Opened', 'Closed', 'Cancelled'], validators=[DataRequired()])
    submit = SubmitField("Validate")

class TableSaveForm(FlaskForm):
    """
    Table form structure:
        - table_name
        - submit
    """
    table_name = SelectField(
        "Choose Table Name",
        choices=get_table_list(),
        validators=[DataRequired()]
    )
    submit = SubmitField("Next")