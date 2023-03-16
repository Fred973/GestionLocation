from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SubmitField, SelectField, DateField
from wtforms.validators import DataRequired
from wtforms.widgets import TextArea


class TasksListForm(FlaskForm):
    # """
    # QuestionList form structure:
    #     - question
    #     - answer
    #     - remarks
    # """
    # question = StringField("Question", widget=TextArea())
    # answer = StringField("Answer", widget=TextArea())
    # remark = StringField("Remarks", widget=TextArea())
    submit = SubmitField("Save task")
