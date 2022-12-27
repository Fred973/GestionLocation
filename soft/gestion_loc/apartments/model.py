from soft import db


class Apartments(db.Model):
    """
    Apartments Database structure:
        - id
        - apartment_name
        - rent_price
        - address
        - zipcode
        - city
    """
    id = db.Column(db.Integer, primary_key=True)
    apartment_name = db.Column(db.String(255), nullable=False, unique=True)
    rent_price = db.Column(db.Numeric(10, 2))
    month = db.Column(db.Boolean, nullable=False)
    day = db.Column(db.Boolean, nullable=False)
    address = db.Column(db.String(255), nullable=False)
    zipcode = db.Column(db.Numeric(5, 0), nullable=False)
    city = db.Column(db.String(255), nullable=False)

    invoices_in = db.relationship('InvoicesIn', backref='apartments', passive_deletes=True)
    invoices_out = db.relationship('InvoicesOut', backref='apartments', passive_deletes=True)
    tenants = db.relationship('Tenants', backref='apartments', passive_deletes=True)
    contracts = db.relationship('Contracts', backref='apartments', passive_deletes=True)
    receipts = db.relationship('Receipts', backref='apartments', passive_deletes=True)

    def __repr__(self):
        return '<Apartments %r>' % self.address
