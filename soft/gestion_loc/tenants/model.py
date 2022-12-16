from soft import db


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
        return '<Tenants %r>' % self.apartment_name
