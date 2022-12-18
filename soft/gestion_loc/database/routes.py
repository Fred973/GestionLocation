import os

from flask import render_template, request, flash, redirect, url_for, send_from_directory
from flask_login import login_required

from soft import app, db
from soft.constant import rental_contracts_path, db_save_path
from soft.func.db_func import import_db, export_db, delete_db
from soft.func.various_func import create_contract_nbr, get_date_from_db_save_name
from soft.gestion_loc.contracts.forms import ContractForm
from soft.gestion_loc.apartments.model import Apartments
from soft.gestion_loc.contracts.model import Contracts
from soft.gestion_loc.tenants.model import Tenants


@app.route('/gestionLoc/Databases', methods=['GET', 'POST'])
@login_required
def databases():
    try:
        file_list = []
        n = 0

        for file in os.listdir(db_save_path):
            file_list.append([file])
            file_list[n].append(get_date_from_db_save_name(file))
            n += 1
        return render_template(
            "gestion_loc/databases/databases.html",
            file_list=file_list
        )
    except Exception as e:
        print(e)
        return render_template(
            "error_404.html",
            log=e
        )


@app.route('/gestionLoc/Databases/save_db', methods=['GET', 'POST'])
@login_required
def save_database():
    try:
        import_db()
        flash('Database saved', category='success')
        return redirect(url_for('databases'))

    except Exception as e:
        print(e)
        return render_template(
            "error_404.html",
            log=e
        )


@app.route('/gestionLoc/Databases/export_db/<string:db_name>', methods=['GET', 'POST'])
@login_required
def export_database(db_name: str):
    try:
        # Get db name to export
        export_db(db_name)
        flash('Database updated', category='success')
        return redirect(url_for('databases'))

    except Exception as e:
        print(e)
        return render_template(
            "error_404.html",
            log=e
        )


@app.route('/gestionLoc/Databases/delete_db/<string:db_name>', methods=['GET', 'POST'])
@login_required
def delete_database_save(db_name: str):
    try:
        # Get db name to export
        delete_db(db_name)
        flash('Database deleted', category='success')
        return redirect(url_for('databases'))

    except Exception as e:
        flash('Problem !!!', category='error')
        print(e)
        return render_template(
            "error_404.html",
            log=e
        )
