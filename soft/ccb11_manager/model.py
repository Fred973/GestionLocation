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

    filenames = db.relationship('TasksFilename', backref='tasks', passive_deletes=True)

    def __repr__(self):
        return '<Tasks %r>' % self.id


class TasksFilename(db.Model):
    """
    TasksFilename Database structure:
        - id
        - fk_task
        - filename
    """
    id = db.Column(db.Integer, primary_key=True)
    fk_task = db.Column(db.Integer, db.ForeignKey('tasks.id', ondelete='CASCADE'), nullable=False)
    filename = db.Column(db.String(255), nullable=True)

    def __repr__(self):
        return '<TasksFilename %r>' % self.filename
