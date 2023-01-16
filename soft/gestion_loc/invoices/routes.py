import datetime
import os
import shutil
import zipfile

from flask import render_template, request, flash, redirect, url_for, send_from_directory, session
from flask_login import login_required, current_user
from soft import app, db
from soft.constant import invoices_in_path, avio_json, invoices_out_path, amount_held_on_account, tmp_path, \
    invoices_out_zip_path
from soft.func.date_func import convert_date_string_to_isoformat, convert_to_month, convert_to_year, today_date
from soft.func.pdf_func import create_invoice_out_pdf
from soft.func.various_func import create_invoice_out_nbr, get_apartment_name, calculate_day_nbr, \
    invoice_out_table_list, \
    invoice_in_table_list, total_apart, total_by_benefits, total_year_forecast_by_benefits, total_year_forecast, \
    total_year_forecast_by_aparts, get_apartment_name_list, mager_dicts, purge_tmp_path, create_invoices_zip_name, \
    create_invoice_in_nbr
from soft.gestion_loc.invoices.forms import InvoiceInForm, InvoiceOutForm, YearForm, DateSelectForm, AllInvoicesOutForm
from soft.gestion_loc.apartments.model import Apartments
from soft.gestion_loc.tenants.model import Tenants
from soft.gestion_loc.invoices.model import InvoicesIn, InvoicesOut
from soft.login.model import Users


@app.route('/gestion_loc/Invoices', methods=['GET', 'POST'])
@login_required
def invoices():
    year_form = YearForm()

    if request.method == 'POST':
        year = int(year_form.year.data)
        return render_template(
            'gestion_loc/invoices/invoices.html',
            invoices_out_list=invoice_out_table_list(year),
            invoices_in_list=invoice_in_table_list(year),
            total_apart=total_apart(year),
            total_by_benefits=total_by_benefits(year),
            total_year_forecast_by_aparts=total_year_forecast_by_aparts(year),
            total_year_forecast_by_benefits=total_year_forecast_by_benefits(year),
            total_year_forecast=total_year_forecast(year),
            year_form=year_form,
            percentage=amount_held_on_account
        )

    return render_template(
        'gestion_loc/invoices/invoices.html',
        invoices_out_list=invoice_out_table_list(2023),
        invoices_in_list=invoice_in_table_list(2023),
        total_apart=total_apart(2023),
        total_by_benefits=total_by_benefits(2023),
            total_year_forecast_by_aparts=total_year_forecast_by_aparts(2023),
        total_year_forecast_by_benefits=total_year_forecast_by_benefits(2023),
        total_year_forecast=total_year_forecast(2023),
        year_form=year_form,
        percentage=amount_held_on_account
    )

@app.route('/gestionLoc/InvoicesIn', methods=['GET', 'POST'])
@login_required
def invoices_in():
    try:
        invoices_in_list = InvoicesIn.query.all()
        return render_template(
            "gestion_loc/invoices/invoices_in.html",
            invoices=invoices_in_list,

        )
    except Exception as e:
        print(e)
        return render_template(
            "error_404.html",
            log=e
        )


@app.route('/gestionLoc/InvoicesIn/add_invoice_in', methods=['GET', 'POST'])
@login_required
def add_invoice_in():
    try:
        form = InvoiceInForm()
        form.aparts_name.choices = get_apartment_name_list()

        if request.method == "POST":
            # Get invoice file name
            if request.files['invoice_file']:
                f = request.files['invoice_file']
                file_to_upload = f.filename
            else:
                file_to_upload = ""

            # Get apartment data
            id_apart = ""
            apartment_name = ""
            req = Apartments.query.filter_by(apartment_name=form.aparts_name.data)
            for i in req:
                apartment_name = i.apartment_name
                id_apart = i.id

            if form.common_invoice.data:
                apartment_name = '7'

            # Get name for who from DB user
            who_name = ''
            who_name_req = Users.query.filter_by(username=session['user'])
            for name in who_name_req:
                who_name = name.name

            invoice_req = InvoicesIn(
                fk_apartment=id_apart,
                who=who_name,
                apartment_name=apartment_name,
                description=form.description.data,
                ref_invoice=form.ref_invoice.data,
                added_date=form.added_date.data,
                tax_deductible=form.tax_deductible.data,
                common_invoice=form.common_invoice.data,
                price=form.price.data,
                year=int(convert_to_year(form.added_date.data)),
                file_name=file_to_upload
            )
            db.session.add(invoice_req)
            db.session.commit()

            try:
                # Create invoice_in_nbr and file name
                invoice_in_name = create_invoice_in_nbr(
                    apart_name=apartment_name,
                    id_user=current_user.id,
                    id_invoice_in=invoice_req.id
                )

                # Upload file to contract path
                f = request.files['invoice_file']
                f.save(os.path.join(invoices_in_path, f.filename))

                # Update DB invoice_in_nbr and filename
                # TODO add record of filename
                invoice_req.invoice_number = invoice_in_name
                db.session.commit()

            except IsADirectoryError:
                flash("Vous n'avez pas télécharger de facture", category="info")

            flash('Facture ajoutée !', category='success')
            return redirect(url_for('invoices_in'))

        return render_template(
            'gestion_loc/invoices/form_invoice_in.html',
            form=form,
            title='Ajouter une facture entrante',
            edit=False
        )
    except Exception as e:
        print(e)
        return render_template(
            "error_404.html",
            log=e
        )


@app.route('/gestionLoc/InvoicesIn/add_invoice_in/<int:id_invoice>', methods=['GET', 'POST'])
@login_required
def edit_invoice_in(id_invoice):
    try:
        form = InvoiceInForm()
        # Get data from invoice_in DB
        invoice_in_to_edit = InvoicesIn.query.get_or_404(id_invoice)

        if request.method == "POST":
            # Upload file to invoice_in path
            if request.files['invoice_file'].filename != invoice_in_to_edit.file_name:
                if request.files['invoice_file'].filename == "":
                    pass
                else:
                    try:
                        # Delete old file
                        os.remove(invoices_in_path + "/" + invoice_in_to_edit.file_name)
                        # Record new file
                        f = request.files['invoice_file']
                        f.save(os.path.join(invoices_in_path, f.filename))
                        # Record data in DB
                        invoice_in_to_edit.file_name = request.files['invoice_file'].filename
                        db.session.commit()
                        db.session.close()
                    except IsADirectoryError:
                        pass


            # Get name for who from DB user
            who_name = ''
            who_name_req = Users.query.filter_by(username=session['user'])
            for name in who_name_req:
                who_name = name.name

            invoice_in_to_edit.common_invoice = form.common_invoice.data
            invoice_in_to_edit.who = who_name
            invoice_in_to_edit.apart_name = form.aparts_name.data
            invoice_in_to_edit.ref_invoice = form.ref_invoice.data
            if form.added_date.data != "":
                invoice_in_to_edit.added_date = form.added_date.data
            invoice_in_to_edit.price = form.price.data
            invoice_in_to_edit.tax_deductible = form.tax_deductible.data

            db.session.commit()

            flash('La facture a bien été éditée !', category='success')
            return redirect(url_for('invoices_in'))

        form.aparts_name.choices = get_apartment_name_list()
        form.common_invoice.data = invoice_in_to_edit.common_invoice
        form.ref_invoice.data = invoice_in_to_edit.ref_invoice
        form.description.data = invoice_in_to_edit.description
        form.price.data = invoice_in_to_edit.price
        form.tax_deductible.data = invoice_in_to_edit.tax_deductible
        if invoice_in_to_edit.file_name is not None:
            form.file_name.data = invoice_in_to_edit.file_name

        return render_template(
            'gestion_loc/invoices/form_invoice_in.html',
            form=form,
            title='Editer une facture entrante',
            edit=True
        )
    except Exception as e:
        print(e)
        return render_template(
            "error_404.html",
            log=e
        )


@app.route('/gestion_loc/InvoicesIn/download_invoice_in/<int:id_invoice>', methods=['GET', 'POST'])
@login_required
def download_invoice_in(id_invoice):
    try:
        # Get contract to download
        invoice_in_to_download = InvoicesIn.query.get_or_404(id_invoice)
        return send_from_directory(
            invoices_in_path, invoice_in_to_download.file_name
        )
    except Exception as e:
        print(e)
        return render_template(
            "error_404.html",
            log=e
        )


@app.route('/gestionLoc/InvoicesIn/delete_invoice_in/<int:id_invoice>', methods=['GET'])
@login_required
def delete_invoice_in(id_invoice):
    try:
        invoice_in_to_delete = InvoicesIn.query.get_or_404(id_invoice)
        # Delete contract of DB
        db.session.delete(invoice_in_to_delete)
        db.session.commit()
        # Delete file from rental_contract path
        try:
            os.remove(invoices_in_path + '/' + invoice_in_to_delete.file_name)
            flash('La facture a bien été supprimé', category='success')
            return redirect(url_for('invoices_in'))
        except IsADirectoryError:
            flash('La facture a bien été supprimé', category='success')
            return redirect(url_for('invoices_in'))
    except Exception as e:
        print(e)
        return render_template(
            "error_404.html",
            log=e
        )


@app.route('/gestionLoc/InvoicesOut', methods=['GET', 'POST'])
@login_required
def invoices_out():
    try:
        invoices_out_list = InvoicesOut.query.all()
        return render_template(
            "gestion_loc/invoices/invoices_out.html",
            invoices=invoices_out_list
        )
    except Exception as e:
        print(e)
        return render_template(
            "error_404.html",
            log=e
        )


@app.route('/gestionLoc/InvoicesOut/add_invoice_out', methods=['GET', 'POST'])
@login_required
def add_invoice_out():
    try:
        form = InvoiceOutForm()
        apartment_name_list = Apartments.query.all()
        tenants_list = Tenants.query.all()
        if request.method == 'POST':  # For Avio invoice
            # Get apartment_name
            req = Apartments.query.get_or_404(request.form.get('apartment'))

            # Check if invoice already exists
            invoice_nbr = create_invoice_out_nbr(
                    n=0,
                    apart_name=get_apartment_name(request.form.get('apartment')),
                    date_=request.form.get('due_date')
                )
            invoice_out_req = InvoicesOut.query.all()
            for i in invoice_out_req:
                if invoice_nbr in i.invoice_number:
                    flash('Cette facture existe déjà !', category='warning')
                    return redirect(url_for('invoices_out'))

            # Record in DB invoice_out
            invoice_req = InvoicesOut(
                fk_apartment=request.form.get('apartment'),
                apartment_name=req.apartment_name,
                ref_customer=form.ref_customer.data,
                name=avio_json['name'],
                address=avio_json['address'],
                zipcode=avio_json['zipcode'],
                city=avio_json['city'],
                invoice_number=invoice_nbr,
                added_date=datetime.date.today(),
                date_in=convert_date_string_to_isoformat(form.date_in.data),
                date_out=convert_date_string_to_isoformat(form.date_out.data),
                due_date=convert_date_string_to_isoformat(form.due_date.data),
                year=int(convert_to_year(request.form.get('date_in'))),
                month=convert_to_month(request.form.get('date_in')),
                price=req.rent_price,
                file_name='{}.pdf'.format(create_invoice_out_nbr(
                    n=0,
                    apart_name=get_apartment_name(request.form.get('apartment')),
                    date_=request.form.get('due_date')
                ))
            )
            db.session.add(invoice_req)
            db.session.commit()

            file = create_invoice_out_pdf(
                id_apart=request.form.get('apartment'),
                date_in=request.form.get('date_in'),
                date_out=request.form.get('date_out'),
                due_date=request.form.get('due_date'),
                price=req.rent_price,
                ref_customer=form.ref_customer.data
            )
            # return send_from_directory(invoices_out_path, file)
            flash(f"La facture pour l'appartement {req.apartment_name} a bien été ajouté", category='success')
            return redirect(url_for('invoices_out'))

        return render_template(
            'gestion_loc/invoices/form_invoice_out.html',
            form=form,
            aparts=apartment_name_list,
            tenants=tenants_list
        )
    except Exception as e:
        print(e)
        return render_template(
            "error_404.html",
            log=e
        )


@app.route('/gestion_loc/InvoicesOut/download_invoice_out/<int:id_invoice>', methods=['GET', 'POST'])
@login_required
def download_invoice_out(id_invoice):
    try:
        # Get contract to download
        invoice_out_to_download = InvoicesOut.query.get_or_404(id_invoice)
        return send_from_directory(
            invoices_out_path, invoice_out_to_download.file_name
        )
    except Exception as e:
        print(e)
        return render_template(
            "error_404.html",
            log=e
        )


@app.route('/gestionLoc/InvoicesOut/delete_invoice_out/<int:id_invoice>', methods=['GET', 'POST'])
@login_required
def delete_invoice_out(id_invoice):
    try:
        invoice_out_to_delete = InvoicesOut.query.get_or_404(id_invoice)
        # Delete contract of DB
        db.session.delete(invoice_out_to_delete)
        db.session.commit()
        # Delete file from rental_contract path
        os.remove(invoices_out_path + '/' + invoice_out_to_delete.file_name)
        flash('La facture a bien été supprimé', category='success')
        return redirect(request.referrer)
    except Exception as e:
        print(e)
        return render_template(
            "error_404.html",
            log=e
        )


@app.route('/gestionLoc/InvoicesOut/download_invoices_out_index', methods=['GET', 'POST'])
@login_required
def download_invoices_out_index():
    try:
        def remove_same_value(items):
            seen = []
            for item in items:
                if item not in seen:
                    seen.append(item)
            return list(seen)

        form = AllInvoicesOutForm()
        select_form = DateSelectForm()

        month_year_list = []
        for i in InvoicesOut.query.all():
            month_year_list.append(i.month + str(i.year))
        month_year_list = remove_same_value(month_year_list)

        if request.method == 'POST':
            # Get list of all invoices_out PDF created in folder
            month, year = select_form.month_list.data.split('/')
            invoices_out_req = InvoicesOut.query.filter_by(year=int(year)).filter_by(month=str(month + "/"))
            # Update session
            invoices_list = []
            for i in invoices_out_req:
                invoices_list.append(i.file_name)
            session.pop("InvoicesOutList", None)
            dict_invoices_out_list = {
                "file": invoices_list
            }

            if 'InvoicesOutList' in session:
                for key, item in session['InvoicesOutList'].items():
                        session.modified = True
                else:
                    session['InvoicesOutList'] = mager_dicts(session['InvoicesOutList'], dict_invoices_out_list)
            else:
                session['InvoicesOutList'] = dict_invoices_out_list

            select_form.month_list.choices = month_year_list

            return render_template(
                'gestion_loc/invoices/download_invoices.html',
                select_form=select_form,
                invoices=invoices_out_req,
                form=form
            )

        # Get list of all invoices_out PDF created in folder and to session
        month, year = month_year_list[0].split('/')
        invoices_out_req = InvoicesOut.query.filter_by(year=int(year)).filter_by(month=str(month + "/"))
        invoices_list = []
        for i in invoices_out_req:
            invoices_list.append(i.file_name)
        session.pop("InvoicesOutList", None)
        dict_invoices_out_list = {
            "file": invoices_list
        }

        if 'InvoicesOutList' in session:
            for key, item in session['InvoicesOutList'].items():
                    session.modified = True
            else:
                session['InvoicesOutList'] = mager_dicts(session['InvoicesOutList'], dict_invoices_out_list)
        else:
            session['InvoicesOutList'] = dict_invoices_out_list


        # set form value by default
        select_form.month_list.choices = month_year_list

        return render_template(
            'gestion_loc/invoices/download_invoices.html',
            invoices=invoices_out_req,
            select_form=select_form,
            form=form
        )
    except Exception as e:
        print(e)
        return render_template(
            "error_404.html",
            log=e
        )


@app.route('/gestionLoc/InvoicesOut/download_invoices_list', methods=['GET', 'POST'])
@login_required
def download_invoices_list():
    try:
        invoices_to_zip = []
        for i in session['InvoicesOutList']['file']:
            invoices_to_zip.append(i)

        # Remove all files from tmp_path
        purge_tmp_path()

        # Create zip file name
        zip_file = invoices_out_zip_path + create_invoices_zip_name()
        zipf = zipfile.ZipFile(zip_file, 'w', zipfile.ZIP_DEFLATED)
        # copy invoices pdf to tmp path
        for file in invoices_to_zip:
            shutil.copy2(invoices_out_path + '/' + file, tmp_path + file)
        # create zip file
        for file_to_zip in os.listdir(tmp_path):
            file_to_zip_full_path = os.path.join(tmp_path, file_to_zip)
            # arcname argument specifies what will be the name of the file inside the zipfile
            zipf.write(filename=file_to_zip_full_path, arcname=file_to_zip)

        zipf.close()

        # Remove all files from tmp_path and pop cookie session
        purge_tmp_path()
        #session.pop("InvoicesOutList", None)

        # download zipfile
        return send_from_directory(invoices_out_zip_path, create_invoices_zip_name())

    except Exception as e:
        print(e)
        return render_template(
            "error_404.html",
            log=e
        )
