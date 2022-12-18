from soft import db


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
    contract_nbr = db.Column(db.String(255), nullable=True, unique=True)
    file_name = db.Column(db.String(255), nullable=False, unique=True)

    # Create a String
    def __repr__(self):
        return '<Contracts %r>' % self.contract_nbr
