from soft import db


class Tasks(db.Model):
    """
    Tasks Database structure:
        - id
        - type
        - description
        - added_date
        - relevance
        - closed_date
        - remarks
        - status
    """
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    added_date = db.Column(db.Date, nullable=False)
    relevance = db.Column(db.String(255), nullable=False)
    closed_date = db.Column(db.Date, nullable=True)
    remarks = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return '<Tasks %r>' % self.id
