import os

from flask_login import login_required
from soft import app, db
from flask import render_template, redirect, url_for, flash, session, request, send_from_directory

from soft.constant import rental_contracts_path
from soft.gestion_loc.forms import ApartmentForm, ContractForm
from soft.gestion_loc.model import Contracts, Invoices, Tenants, Apartments


@app.route('/gestionLoc/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    try:
        return render_template(
            'gestion_loc/dashboard.html'
        )
    except Exception as e:
        print(e)
        return render_template(
            "error_404.html",
            log=e
        )

@login_required
@app.route('/gestionLoc/Apartments', methods=['GET', 'POST'])
def apartments():
    apartment_list = Apartments.query.all()
    return render_template(
        "gestion_loc/apartments/apartments.html",
        aparts=apartment_list
    )

@login_required
@app.route('/gestionLoc/Apartments/add_Apartment', methods=['GET', 'POST'])
def add_apartment():
    form = ApartmentForm()
    if form.validate_on_submit():
        apart_to_add = Apartments(
            apartment_name=form.apartment_name.data,
            address=form.address.data,
            zipcode=form.zipcode.data,
            city=form.city.data,
            rent_price=form.rent_price.data
        )
        # Clear the form
        form.apartment_name.data = ''
        form.address.data = ''
        form.zipcode.data = ''
        form.city.data = ''
        # Add data to DB
        db.session.add(apart_to_add)
        db.session.commit()
        flash('Appartment ajouté !', category='success')
        return redirect(url_for('apartments'))

    return render_template(
        "gestion_loc/apartments/form_apartment.html",
        form=form,
        title='Ajouter un Appartement'
    )

@login_required
@app.route('/gestionLoc/Apartments/edit_apartment/<int:id_apart>', methods=['GET', 'POST'])
def edit_apartment(id_apart):
    form = ApartmentForm()
    apart_to_edit = Apartments.query.get_or_404(id_apart)
    if form.validate_on_submit():
        apart_to_edit.apartment_name = form.apartment_name.data
        apart_to_edit.address = form.address.data
        apart_to_edit.zipcode = form.zipcode.data
        apart_to_edit.city = form.city.data
        apart_to_edit.rent_price = form.rent_price.data
        db.session.commit()

        # Clear the form
        form.apartment_name.data = ''
        form.address.data = ''
        form.zipcode.data = ''
        form.city.data = ''
        form.rent_price.data = ''
        flash("L'appartement a bien été modifié", category='success')
        return redirect(url_for('apartments'))

    form.apartment_name.data = apart_to_edit.apartment_name
    form.address.data = apart_to_edit.address
    form.zipcode.data = apart_to_edit.zipcode
    form.city.data = apart_to_edit.city
    form.rent_price.data = apart_to_edit.rent_price
    return render_template(
        'gestion_loc/apartments/form_apartment.html',
        form=form,
        title='Modifier'
    )

@login_required
@app.route('/gestionLoc/Apartments/delete_apartment/<int:id_apart>', methods=['GET'])
def delete_apartment(id_apart):
    apart_to_delete = Apartments.query.get_or_404(id_apart)
    db.session.delete(apart_to_delete)
    db.session.commit()
    return redirect(request.referrer)

@login_required
@app.route('/gestionLoc/Contracts', methods=['GET', 'POST'])
def contracts():
    rental_contract = Contracts.query.all()
    return render_template(
        "gestion_loc/contracts/contracts.html",
        contracts=rental_contract
    )

@login_required
@app.route('/gestionLoc/Contracts/add_contract', methods=['GET', 'POST'])
def add_contract():
    form = ContractForm()
    apartment_name_list = Apartments.query.all()

    if request.method == "POST":
        # Get contract file name
        f = request.files['contract_file']
        # Get apartment_name
        req = Apartments.query.get_or_404(request.form.get('apartment'))

        contract_req = Contracts(
            fk_apartment=request.form.get('apartment'),
            apartment_name=req.apartment_name,
            contract_nbr=form.contract_nbr.data,
            file_name=f.filename
        )
        db.session.add(contract_req)
        db.session.commit()

        # Upload file to contract path
        f.save(os.path.join(rental_contracts_path, f.filename))

        flash('Contrat de location ajouté !', category='success')
        return redirect(url_for('contracts'))

    return render_template(
        "gestion_loc/contracts/form_contract.html",
        title='Ajouter un contrat',
        form=form,
        aparts = apartment_name_list
    )


@login_required
@app.route('/gestion_loc/Contracts/download_contract/<int:id_contract>', methods=['GET', 'POST'])
def download_contract(id_contract):
    # Get contract to download
    contract_to_download = Contracts.query.get_or_404(id_contract)
    return send_from_directory(
        rental_contracts_path, contract_to_download.file_name
    )


@login_required
@app.route('/gestionLoc/Contracts/delete_contract/<int:id_contract>', methods=['GET'])
def delete_contract(id_contract):
    apart_to_delete = Apartments.query.get_or_404(id_contract)
    # Delete contract of DB
    db.session.delete(apart_to_delete)
    db.session.commit()
    # Delete file from rental_contract path
    os.remove(rental_contracts_path + '/' + apart_to_delete.file_name)
    return redirect(request.referrer)

@login_required
@app.route('/gestionLoc/Tenants', methods=['GET', 'POST'])
def tenants():
    return render_template(
        "gestion_loc/tenants/tenants.html"
    )

@login_required
@app.route('/gestionLoc/Invoices', methods=['GET', 'POST'])
def invoices():
    return render_template(
        "gestion_loc/invoices/invoices.html"
    )
