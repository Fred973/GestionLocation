import os

from flask import render_template, request, flash, redirect, url_for, send_from_directory
from flask_login import login_required

from soft import app, db
from soft.constant import rental_contracts_path
from soft.gestion_loc.contracts.forms import ContractForm
from soft.gestion_loc.apartments.model import Apartments
from soft.gestion_loc.contracts.model import Contracts


@app.route('/gestionLoc/Contracts', methods=['GET', 'POST'])
@login_required
def contracts():
    try:
        rental_contract_list = Contracts.query.all()

        return render_template(
            "gestion_loc/contracts/contracts.html",
            contracts=rental_contract_list
        )
    except Exception as e:
        print(e)
        return render_template(
            "error_404.html",
            log=e
        )


@app.route('/gestionLoc/Contracts/add_contract', methods=['GET', 'POST'])
@login_required
def add_contract():
    try:
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
    except Exception as e:
        print(e)
        return render_template(
            "error_404.html",
            log=e
        )


@app.route('/gestion_loc/Contracts/download_contract/<int:id_contract>', methods=['GET', 'POST'])
@login_required
def download_contract(id_contract):
    try:
        # Get contract to download
        contract_to_download = Contracts.query.get_or_404(id_contract)
        return send_from_directory(
            rental_contracts_path, contract_to_download.file_name
        )
    except Exception as e:
        print(e)
        return render_template(
            "error_404.html",
            log=e
        )


@app.route('/gestionLoc/Contracts/delete_contract/<int:id_contract>', methods=['GET'])
@login_required
def delete_contract(id_contract):
    try:
        contract_to_delete = Contracts.query.get_or_404(id_contract)
        # Delete contract of DB
        db.session.delete(contract_to_delete)
        db.session.commit()
        # Delete file from rental_contract path
        os.remove(rental_contracts_path + '/' + contract_to_delete.file_name)
        flash('Le contrat de location a bien été supprimé', category='success')
        return redirect(request.referrer)
    except Exception as e:
        print(e)
        return render_template(
            "error_404.html",
            log=e
        )
