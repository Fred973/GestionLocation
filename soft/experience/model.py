from soft import db


class TechLog(db.Model):
    """
    TechLog Database structure:
        - id
        - date
        - ac_type
        - registration
        - ata
        - work_order
        - description
        - work_type
        - time
        - function
    """
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    ac_type = db.Column(db.String(255), nullable=False)
    registration = db.Column(db.String(255), nullable=False)
    ata = db.Column(db.String(255), nullable=False)
    work_order = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    work_type = db.Column(db.String(255), nullable=False)
    time =  db.Column(db.Numeric(3, 2), nullable=False)
    function = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return '<TechLog %r>' % self.date
