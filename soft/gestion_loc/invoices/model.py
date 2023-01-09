from soft import db


class InvoicesIn(db.Model):
    """
    Invoices In Database structure:
        - id
        - fk_apartment --> foreign key with Apartments id
        - who
        - apartment_name
        - invoice_number
        - description
        - added_date
        - file_name
    """
    id = db.Column(db.Integer, primary_key=True)
    fk_apartment = db.Column(db.Integer, db.ForeignKey('apartments.id', ondelete='CASCADE'), nullable=False)
    who = db.Column(db.String(255), nullable=False)
    apartment_name = db.Column(db.String(255), nullable=False)
    invoice_number = db.Column(db.String(255), nullable=True)
    description = db.Column(db.String(255), nullable=True)
    added_date = db.Column(db.Date, nullable=False)
    year = db.Column(db.Numeric(4, 0), nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    tax_deductible = db.Column(db.Boolean, nullable=False)
    common_invoice = db.Column(db.Boolean, nullable=False)
    file_name = db.Column(db.String(128), nullable=True)

    # Create a String
    def __repr__(self):
        return '<InvoicesIn %r>' % self.invoice_number


class InvoicesOut(db.Model):
    """
    Invoices Out Database structure:
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
    apartment_name = db.Column(db.String(255), nullable=True)
    ref_customer = db.Column(db.String(255), nullable=True)
    first_name = db.Column(db.String(255), nullable=True)
    name = db.Column(db.String(255), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    zipcode = db.Column(db.Numeric(5, 0), nullable=False)
    city = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(255), nullable=True)
    email = db.Column(db.String(255), nullable=True)
    invoice_number = db.Column(db.String(255), nullable=True, unique=True)
    added_date = db.Column(db.Date, nullable=False)
    date_in = db.Column(db.Date, nullable=True)
    date_out = db.Column(db.Date, nullable=True)
    due_date = db.Column(db.Date, nullable=True)
    month = db.Column(db.String(255), nullable=True)
    year = db.Column(db.Numeric(4, 0), nullable=False)
    price = db.Column(db.Numeric(10, 2))
    file_name = db.Column(db.String(128), nullable=False)

    # Create a String
    def __repr__(self):
        return '<InvoicesOut %r>' % self.name
