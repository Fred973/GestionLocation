import datetime
import os
from flask import render_template, request, flash, redirect, url_for, send_from_directory
from flask_login import login_required
from soft import app, db
from soft.constant import invoices_in_path, avio_json, invoices_out_path, amount_held_on_account
from soft.func.date_func import convert_date_string_to_isoformat, convert_to_month, convert_to_year
from soft.func.pdf_func import create_invoice_out_pdf
from soft.func.various_func import create_invoice_out_nbr, get_apartment_name, calculate_day_nbr, invoice_out_table_list, \
    invoice_in_table_list, total_apart, total_by_benefits, total_year_forecast_by_benefits, total_year_forecast, \
    total_year_forecast_by_aparts, get_apartment_name_list
from soft.gestion_loc.invoices.forms import InvoiceInForm, InvoiceOutForm, YearForm
from soft.gestion_loc.apartments.model import Apartments
from soft.gestion_loc.tenants.model import Tenants
from soft.gestion_loc.invoices.model import InvoicesIn, InvoicesOut


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
            req = Apartments.query.filter_by(apartment_name=form.aparts_name.data)
            id_apart = ""
            apartment_name = ""
            for i in req:
                apartment_name = i.apartment_name
                id_apart = i.id

            invoice_req = InvoicesIn(
                fk_apartment=id_apart,
                who=form.who.data,
                apartment_name=apartment_name,
                invoice_number=form.invoice_number.data,
                description=form.description.data,
                added_date=form.added_date.data,
                tax_deductible=form.tax_deductible.data,
                price=form.price.data,
                year=int(convert_to_year(form.added_date.data)),
                file_name=file_to_upload
            )
            db.session.add(invoice_req)
            db.session.commit()

            try:
                # Upload file to contract path
                f = request.files['invoice_file']
                f.save(os.path.join(invoices_in_path, f.filename))
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
                    except IsADirectoryError:
                        pass
                    # Record new file
                    f = request.files['invoice_file']
                    f.save(os.path.join(invoices_in_path, f.filename))
                    # Record data in DB
                    invoice_in_to_edit.file_name = request.files['invoice_file'].filename
                    db.session.commit()
                    db.session.close()

            invoice_in_to_edit.who = form.who.data
            invoice_in_to_edit.apart_name = form.aparts_name.data
            invoice_in_to_edit.invoice_number = form.invoice_number.data
            if form.added_date.data != "":
                invoice_in_to_edit.added_date = form.added_date.data
            invoice_in_to_edit.price = form.price.data
            invoice_in_to_edit.tax_deductible = form.tax_deductible.data

            db.session.commit()

            flash('La facture a bien été éditée !', category='success')
            return redirect(url_for('invoices_in'))

        form.aparts_name.choices = get_apartment_name_list()
        form.who.data = invoice_in_to_edit.who
        form.invoice_number.data = invoice_in_to_edit.invoice_number
        form.description.data = invoice_in_to_edit.description
        # form.added_date.default = datetime.date.today().strftime("%d/%m/%YY")
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
            # Record in DB invoice_out
            invoice_req = InvoicesOut(
                fk_apartment=request.form.get('apartment'),
                apartment_name=req.apartment_name,
                ref_customer=form.ref_customer.data,
                name=avio_json['name'],
                address=avio_json['address'],
                zipcode=avio_json['zipcode'],
                city=avio_json['city'],
                invoice_number=create_invoice_out_nbr(
                    n=0,
                    apart_name=get_apartment_name(request.form.get('apartment')),
                    date_=request.form.get('due_date')
                ),
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
