from soft import db

class OrderList(db.Model):
    """
    - id
    - part_number
    - description
    - qty
    - remark
    - job_card
    - order_sent_on
    - received
    - received_on
    - record_by
    - creation_date
    """
    id = db.Column(db.Integer, primary_key=True)
    part_number = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=False)
    qty = db.Column(db.Text, nullable=False)
    remark = db.Column(db.Text, nullable=True)
    job_card = db.Column(db.Integer, nullable=True)
    order_sent_on = db.Column(db.Date, nullable=False)
    received = db.Column(db.Boolean, nullable=True)
    received_on = db.Column(db.Date, nullable=True)
    record_by = db.Column(db.String(255), nullable=False)
    creation_date = db.Column(db.Date, nullable=False)

    def __repr__(self):
        return '<OrderList %r>' % self.part_number