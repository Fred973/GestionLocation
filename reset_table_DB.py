import os

from soft import db, app
from soft.constant import invoices_in_path, rental_contracts_path
from soft.gestion_loc.apartments.model import Apartments
from soft.login.model import Users

with app.app_context():
    db.drop_all()

    db.create_all()

    # Users Table
    user_1 = Users(
    id=1,
    username='fred',
    category=1,
    password_hash='sha256$uvPHv3uhXGtYRt0h$5090871eb4c28b38128af516a3d5c1a4611a81babf273529076e5e1aadc7dc6b'

    )
    user_2 = Users(
    id=2,
    username='jojo',
    category=2,
    password_hash='sha256$uvPHv3uhXGtYRt0h$5090871eb4c28b38128af516a3d5c1a4611a81babf273529076e5e1aadc7dc6b'

    )
    db.session.add(user_1)
    db.session.add(user_2)
    db.session.commit()

    # Apartments Table
    apart_01 = Apartments(
        id=1,
        apartment_name='7A',
        rent_price=1500.00,
        address='7, rue Edgar Degas',
        zipcode=97310,
        city='Kourou',

    )
    apart_02 = Apartments(
        id=2,
        apartment_name='7B',
        rent_price=1200.00,
        address='8, avenue Bourges Maunoury',
        zipcode=31200,
        city='Kourou',

    )
    apart_03 = Apartments(
        id=3,
        apartment_name='10A',
        rent_price=1300.50,
        address='7, rue du truc',
        zipcode=97310,
        city='Kourou',

    )
    db.session.add(apart_01)
    db.session.add(apart_02)
    db.session.add(apart_03)
    db.session.commit()

    # Delete all files in folders : invoices & rental_contracts
    for f in os.listdir(invoices_in_path):
        if f:
            os.remove(os.path.join(invoices_in_path, f))
    for f in os.listdir(rental_contracts_path):
        if f:
            os.remove(os.path.join(rental_contracts_path, f))