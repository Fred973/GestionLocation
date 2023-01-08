import os

from flask import render_template, request, flash, redirect, url_for, send_from_directory
from flask_login import login_required

from soft import app, db
from soft.constant import rental_contracts_path
from soft.func.various_func import create_contract_nbr, compare_list
from soft.gestion_loc.contracts.forms import ContractForm
from soft.gestion_loc.apartments.model import Apartments
from soft.gestion_loc.contracts.model import Contracts
from soft.gestion_loc.tenants.model import Tenants


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
    # try:
        form = ContractForm()
        # Create apartment list for combobox
        apartment_name_list = []
        contracts_list = []
        apartment_name_req = Apartments.query.all()
        contracts_req = Contracts.query.all()
        for i in apartment_name_req:
            apartment_name_list.append(i.apartment_name)

        for i in contracts_req:
            contracts_list.append(i.apartment_name)

        aparts_list = compare_list(apartment_name_list, contracts_list)

        # Send apartment list to combobox
        form.apartment.choices = aparts_list

        if request.method == "POST":
            # Get contract file name
            f = request.files['contract_file']

            # Get id apartment for fk_apartment
            aparts_req = Apartments.query.filter_by(apartment_name=form.apartment.data)
            apart_id = [i.id for i in aparts_req]

            contract_req = Contracts(
                fk_apartment=int(apart_id[0]),
                apartment_name=form.apartment.data,
                contract_nbr=create_contract_nbr(
                    apart_name=form.apartment.data
                ),
                file_name=create_contract_nbr(apart_name=form.apartment.data) + ".pdf"
            )
            db.session.add(contract_req)
            db.session.commit()

            # Upload file to contract path
            f.save(os.path.join(rental_contracts_path, create_contract_nbr( apart_name=form.apartment.data) + ".pdf"))

            flash('Contrat de location ajouté !', category='success')
            return redirect(url_for('contracts'))

        return render_template(
            "gestion_loc/contracts/form_contract.html",
            title='Ajouter un contrat',
            form=form
        )
    # except Exception as e:
    #     print(e)
    #     return render_template(
    #         "error_404.html",
    #         log=e
    #     )


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
