from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SubmitField, SelectField, DateField
from wtforms.validators import DataRequired
from wtforms.widgets import TextArea

from soft.func.db_func import get_table_list

class QuestionsListForm(FlaskForm):
    """
    QuestionsList form structure:
        - question
        - answer
        - remarks
    """
    question = StringField("Question", widget=TextArea())
    answer = StringField("Answer", widget=TextArea())
    remark = StringField("Remarks", widget=TextArea())
    submit = SubmitField("Add question")
