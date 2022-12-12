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
    rent_price = db.Column(db.Numeric(6, 2))
    address = db.Column(db.String(255), nullable=False)
    zipcode = db.Column(db.Numeric(5, 0), nullable=False)
    city = db.Column(db.String(255), nullable=False)

    invoices = db.relationship('Invoices', backref='apartments', passive_deletes=True)
    tenants = db.relationship('Tenants', backref='apartments', passive_deletes=True)
    contracts = db.relationship('Contracts', backref='apartments', passive_deletes=True)

    def __repr__(self):
        return '<Apartments %r>' % self.address


class Contracts(db.Model):
    """
    Contracts Database structure:
        - id
        - fk_apartment --> foreign key with Apartments id
        - apartment_name
        - contract_nbr
        - file_name

    """
    id = db.Column(db.Integer, primary_key=True)
    fk_apartment = db.Column(db.Integer, db.ForeignKey('apartments.id', ondelete='CASCADE'), nullable=False)
    apartment_name = db.Column(db.String(255), nullable=False, unique=True)
    contract_nbr = db.Column(db.Integer, nullable=True, unique=True)
    file_name = db.Column(db.String(255), nullable=False, unique=True)

    # Create a String
    def __repr__(self):
        return '<Contracts %r>' % self.contract_nbr


class Tenants(db.Model):
    """
    Tenants Database structure:
        - id
        - fk_apartment --> foreign key with Apartments id
        - apartment_name
        - first_name
        - name
        - phone
        - email

    """
    id = db.Column(db.Integer, primary_key=True)
    fk_apartment = db.Column(db.Integer, db.ForeignKey('apartments.id', ondelete='CASCADE'), nullable=False)
    apartment_name = db.Column(db.String(255), nullable=False, unique=True)
    first_name = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(255), nullable=False, unique=True)
    email = db.Column(db.String(255), nullable=False, unique=True)

    # Create a String
    def __repr__(self):
        return '<Invoices %r>' % self.invoice_number


class Invoices(db.Model):
    """
    Invoices Database structure:
        - id
        - fk_apartment --> foreign key with Apartments id
        - apartment_name
        - invoice_number
        - description
        - added_date
        - file_name
    """
    id = db.Column(db.Integer, primary_key=True)
    fk_apartment = db.Column(db.Integer, db.ForeignKey('apartments.id', ondelete='CASCADE'), nullable=False)
    apartment_name = db.Column(db.String(255), nullable=False, unique=True)
    invoice_number = db.Column(db.String(255), nullable=True, unique=True)
    description = db.Column(db.String(128), nullable=True, unique=True)
    added_date = db.Column(db.Date, nullable=False, unique=True)
    file_name = db.Column(db.String(128), nullable=False, unique=True)

    # Create a String
    def __repr__(self):
        return '<Invoices %r>' % self.invoice_number