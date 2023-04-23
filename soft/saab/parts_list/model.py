from soft import db


class PartsList(db.Model):
    """
    - id
    - fk_job_card
    - pn
    - sn
    - description
    - qty
    - reason
    - remarks
    """
    id = db.Column(db.Integer, primary_key=True)
    fk_job_card = db.Column(db.Integer, db.ForeignKey('job_card_list.item_jc', ondelete='CASCADE'), nullable=False)
    pn = db.Column(db.String(255), nullable=False)
    sn = db.Column(db.String(255), nullable=True)
    description = db.Column(db.String(255), nullable=False)
    qty = db.Column(db.Integer, nullable=False)
    reason = db.Column(db.String(255), nullable=False)
    remarks = db.Column(db.String(255), nullable=True)

    def __repr__(self):
        return '<PartsList %r>' % self.fk_job_card
