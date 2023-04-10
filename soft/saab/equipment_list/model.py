from soft import db


class EquipmentList(db.Model):
    """
    - id
    - ata
    - description
    - part_number
    - alternate_pn
    - serial_number
    - batch
    - location
    - remarks
    """
    id = db.Column(db.Integer, primary_key=True)
    ata = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(255), nullable=False)
    part_number = db.Column(db.String(255), nullable=False)
    alternate_pn = db.Column(db.String(255), nullable=True)
    serial_number = db.Column(db.String(255), nullable=True)
    batch = db.Column(db.String(255), nullable=True)
    location = db.Column(db.String(255), nullable=True)
    remarks = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return '<EquipmentList %r>' % self.ata
