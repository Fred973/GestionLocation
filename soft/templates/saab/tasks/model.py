from soft import db
from sqlalchemy import func

class JobCardList(db.Model):
    """
    - id
    - item_jc
    - description
    - remarks
    - working_time
    - performed
    """
    id = db.Column(db.Integer, primary_key=True)
    item_jc = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(255), nullable=False)
    remarks = db.Column(db.Text, nullable=True)
    working_time = db.Column(db.Time, nullable=True)
    accomplishment = db.Column(db.Integer, nullable=True)


    task_details = db.relationship('JobCardDetails', backref='job_card_list', passive_deletes=True)

    def __repr__(self):
        return '<JobCardList %r>' % self.item_jc


class JobCardDetails(db.Model):
    """
    - id
    - job_card
    - type
    - description
    - remarks
    - working_time
    - nbr_tech
    - performed
    """
    id = db.Column(db.Integer, primary_key=True)
    fk_task = db.Column(db.Integer, db.ForeignKey('job_card_list.id', ondelete='CASCADE'), nullable=False)
    job_card = db.Column(db.String(255), nullable=False)
    type = db.Column(db.String(255), nullable=False)
    mm_ref = db.Column(db.String(255), nullable=True)
    description = db.Column(db.String(255), nullable=False)
    remarks = db.Column(db.Text, nullable=True)
    working_time = db.Column(db.Time, nullable=True)
    nbr_tech = db.Column(db.Numeric(2), nullable=True)
    performed = db.Column(db.Boolean, nullable=True)

    def __repr__(self):
        return '<JobCardDetails %r>' % self.job_card