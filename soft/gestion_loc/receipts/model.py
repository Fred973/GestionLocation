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
    fk_apartment = db.Column(db.Integer, db.ForeignKey('apartments.id', ondelete='CASCADE'), nullable=False)
    apartment_name = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    lessor_id = db.Column(db.Integer, nullable=False)
    tenant_id = db.Column(db.Integer, nullable=False)
    added_date = db.Column(db.Date, nullable=False)
    date_in = db.Column(db.Date, nullable=False)
    date_out = db.Column(db.Date, nullable=False)
    month_year = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Numeric(6, 2))
    loads = db.Column(db.Numeric(6, 2))
    contract_nbr = db.Column(db.String(255), nullable=False)
    file_name = db.Column(db.String(255), nullable=False)

    # Create a String
    def __repr__(self):
        return '<Receipts %r>' % self.apartment_name
