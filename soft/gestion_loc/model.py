from soft import db


class Apartments(db.Model):
    """
    Apartments Database structure:
        - id
        - number
        - address
    """
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer, nullable=False, unique=True)
    rent = db.Column(db.Numeric(6, 2), nullable=False)

    invoices = db.relationship('Invoices', backref='apartments', passive_deletes=True)
    tenants = db.relationship('Tenants', backref='apartments', passive_deletes=True)

    def __repr__(self):
        return '<Apartments %r>' % self.number


class Invoices(db.Model):
    """
    Invoices Database structure:
        - id
        - fk_apartment --> foreign key with Apartments id
        - address
        - zipcode
        - city
        - invoice_number
        - added_date
        - file_name

    """
    id = db.Column(db.Integer, primary_key=True)
    fk_apartment = db.Column(db.Integer, db.ForeignKey('apartments.id', ondelete='CASCADE'), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    address = db.Column(db.String(255), nullable=False)
    zipcode = db.Column(db.Numeric(5, 0), nullable=False)
    city = db.Column(db.String(255), nullable=False)
    invoice_number = db.Column(db.Integer, nullable=False, unique=True)
    added_date = db.Column(db.Date, nullable=False, unique=True)
    file_name = db.Column(db.String(128), nullable=False, unique=True)

    # Create a String
    def __repr__(self):
        return '<Invoices %r>' % self.invoice_number


class Tenants(db.Model):
    """
    Tenants Database structure:
        - id
        - fk_apartment --> foreign key with Apartments id
        - first_name
        - name
        - phone
        - email

    """
    id = db.Column(db.Integer, primary_key=True)
    fk_apartment = db.Column(db.Integer, db.ForeignKey('apartments.id', ondelete='CASCADE'), nullable=False)
    first_name = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(255), nullable=False, unique=True)
    email = db.Column(db.String(255), nullable=False, unique=True)

    # Create a String
    def __repr__(self):
        return '<Invoices %r>' % self.invoice_number
