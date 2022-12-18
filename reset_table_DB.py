import os
import shutil

from soft import db, app
from soft.constant import invoices_in_path, rental_contracts_path, invoices_out_path, receipts_path
from soft.func.various_func import create_contract_nbr
from soft.gestion_loc.apartments.model import Apartments
from soft.gestion_loc.contracts.model import Contracts
from soft.gestion_loc.tenants.model import Tenants
from soft.login.model import Users

with app.app_context():
    db.drop_all()

    db.create_all()

    # Delete all files in folders : invoices, rental_contracts, receipts
    for f in os.listdir(invoices_in_path):
        if f:
            os.remove(os.path.join(invoices_in_path, f))
    for f in os.listdir(invoices_out_path):
        if f:
            os.remove(os.path.join(invoices_out_path, f))
    for f in os.listdir(rental_contracts_path):
        if f:
            os.remove(os.path.join(rental_contracts_path, f))
    for f in os.listdir(receipts_path):
        if f:
            os.remove(os.path.join(receipts_path, f))

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

    # Tenants table
    tenant_01 = Tenants(
        id=1,
        fk_apartment=1,
        apartment_name='7A',
        first_name='Truc',
        name='Chose',
        phone='06 06 06 06 06',
        email='truc@gmail.com'
    )

    tenant_02 = Tenants(
        id=2,
        fk_apartment=2,
        apartment_name='7B',
        first_name='Bidule',
        name='Machin',
        phone='06 06 06 06 07',
        email='bidule@gmail.com'
    )

    tenant_03 = Tenants(
        id=3,
        fk_apartment=3,
        apartment_name='10A',
        first_name='Tete',
        name='Demort',
        phone='06 06 06 06 08',
        email='demort@gmail.com'
    )
    db.session.add(tenant_01)
    db.session.add(tenant_02)
    db.session.add(tenant_03)
    db.session.commit()

    # Contracts table
    contract_01 = Contracts(
        id=1,
        fk_apartment=1,
        apartment_name='7A',
        contract_nbr=create_contract_nbr(
            apart_name='7A',
            id_customer=1
        ),
        file_name='contrat_01.pdf'
    )
    contract_02 = Contracts(
        id=2,
        fk_apartment=2,
        apartment_name='7B',
        contract_nbr=create_contract_nbr(
            apart_name='7B',
            id_customer=2
        ),
        file_name='contrat_02.pdf'
    )
    contract_03 = Contracts(
        id=3,
        fk_apartment=3,
        apartment_name='10A',
        contract_nbr=create_contract_nbr(
            apart_name='10A',
            id_customer=3
        ),
        file_name='contrat_03.pdf'
    )
    db.session.add(contract_01)
    db.session.add(contract_02)
    db.session.add(contract_03)
    db.session.commit()
    # Copy contract files to directory
    src_path = os.path.abspath(os.path.dirname(__file__)) + '/default_files_src'
    for f in os.listdir(src_path):
        shutil.copy2(src_path + '/' + f, rental_contracts_path + '/' + f)