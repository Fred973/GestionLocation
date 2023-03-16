from soft import db

class QuestionsList(db.Model):
    """
    - id
    - name
    - creation_date
    - question
    - answer
    - remark
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    creation_date = db.Column(db.Date, nullable=False)
    question = db.Column(db.Text, nullable=False)
    answer = db.Column(db.Text, nullable=True)
    remark = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return '<QuestionsList %r>' % self.name