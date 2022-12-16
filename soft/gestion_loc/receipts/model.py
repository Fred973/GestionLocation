from soft import db


class Receipts(db.Model):
    """
    Receipts Database structure:
        - id
        - fk_receipt --> foreign key with Apartments id
        - apartment_name
        - contract_nbr
        - file_name

    """
    id = db.Column(db.Integer, primary_key=True)
    fk_receipt = db.Column(db.Integer, db.ForeignKey('apartments.id', ondelete='CASCADE'), nullable=False)
    apartments_id = db.Column(db.Integer, nullable=False, unique=True)
    lessor_id = db.Column(db.Integer, nullable=False, unique=True)
    tenant_id = db.Column(db.Integer, nullable=False, unique=True)
    added_date = db.Column(db.Date, nullable=False, unique=True)
    date_in = db.Column(db.Date, nullable=False, unique=True)
    date_out = db.Column(db.Date, nullable=False, unique=True)
    price = db.Column(db.Numeric(6, 2))
    loads = db.Column(db.Numeric(6, 2))
    contract_nbr = db.Column(db.Integer, nullable=True, unique=True)
    file_name = db.Column(db.String(255), nullable=False, unique=True)

    # Create a String
    def __repr__(self):
        return '<Receipts %r>' % self.apartment_name
