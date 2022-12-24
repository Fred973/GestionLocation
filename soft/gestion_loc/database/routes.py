import os
from flask import render_template, request, flash, redirect, url_for, send_from_directory
from flask_login import login_required
from soft import app, db
from soft.ccb11_manager.forms import TableSaveForm
from soft.constant import db_save_path, table_save_path
from soft.func.db_func import import_db, export_db, delete_db, get_date_from_db_save_name, get_table_name, import_table, \
    export_table_to_db, delete_table


@app.route('/gestionLoc/Databases', methods=['GET', 'POST'])
@login_required
def databases():
    try:
        db_file_list = []
        db_n = 0

        for file in os.listdir(db_save_path):
            db_file_list.append([file])
            db_file_list[db_n].append(get_date_from_db_save_name(file))
            db_n += 1

        table_file_list = []
        table_n = 0

        for file in os.listdir(table_save_path):
            table_file_list.append([file])
            table_file_list[table_n].append(get_date_from_db_save_name(file))
            table_file_list[table_n].append(get_table_name(str(file)))
            table_n += 1

        return render_template(
            "gestion_loc/databases/databases.html",
            file_list=db_file_list,
            table_list=table_file_list
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


@app.route('/gestionLoc/Databases/save_table', methods=['GET', 'POST'])
@login_required
def save_table():
    try:
        form = TableSaveForm()
        if request.method == 'POST':
            import_table(form.table_name.data)
            flash('Database saved', category='success')
            return redirect(url_for('databases'))

        return render_template(
            'gestion_loc/databases/save_table.html',
            form=form
        )

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


@app.route('/gestionLoc/Databases/export_table/<string:table_name>', methods=['GET', 'POST'])
@login_required
def export_table(table_name: str):
    try:
        # Get db name to export
        export_table_to_db(
            file_name=table_name,
            table_name=get_table_name(table_name)
        )
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


@app.route('/gestionLoc/Databases/delete_table/<string:table_name>', methods=['GET', 'POST'])
@login_required
def delete_table_save(table_name: str):
    try:
        # Get db name to export
        delete_table(table_name)
        flash('Table deleted', category='success')
        return redirect(url_for('databases'))

    except Exception as e:
        flash('Problem !!!', category='error')
        print(e)
        return render_template(
            "error_404.html",
            log=e
        )
