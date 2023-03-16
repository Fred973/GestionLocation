from soft import db

class OrderList(db.Model):
    """
    - id

    """
    id = db.Column(db.Integer, primary_key=True)
    # name = db.Column(db.Text, nullable=False)
    # creation_date = db.Column(db.Date, nullable=False)
    # question = db.Column(db.Text, nullable=False)
    # answer = db.Column(db.Text, nullable=True)
    # remark = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return '<OrderList %r>' % self.id