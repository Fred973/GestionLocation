import os
import datetime
from flask import render_template, redirect, url_for, send_from_directory, flash, request
from flask_login import login_required
from soft import app, db
from soft.constant import receipts_path
from soft.func.date_func import convert_date_to_string, convert_to_month, convert_to_year
from soft.func.pdf_func import create_receipt_pdf
from soft.gestion_loc.apartments.model import Apartments
from soft.gestion_loc.contracts.model import Contracts
from soft.gestion_loc.receipts.forms import ReceiptForm
from soft.gestion_loc.receipts.model import Receipts
from soft.gestion_loc.tenants.model import Tenants


@app.route('/gestionLoc/receipts', methods=['GET', 'POST'])
@login_required
def receipts():
    try:
        receipts_req = Receipts.query.all()
        return render_template(
            'gestion_loc/receipts/receipts.html',
            receipts=receipts_req
        )
    except Exception as e:
        print(e)
        return render_template(
            "error_404.html",
            log=e
        )


@app.route('/gestionLoc/receipts/add_receipt', methods=['GET', 'POST'])
@login_required
def add_receipt():
    try:
        form = ReceiptForm()
        apartment_name_list = Apartments.query.all()
        receipts_list = Receipts.query.all()
        if request.method == 'POST':
            # Get apartment data
            apart_req = Apartments.query.get_or_404(request.form.get('apartment'))
            # Get tenant & contract data
            id_tenant = ''
            contract_nbr = ''
            name_tenant = ''
            tenant_req = Tenants.query.filter_by(fk_apartment=apart_req.id)
            for data in tenant_req:
                id_tenant = data.id
                name_tenant = data.name
            contract_req = Contracts.query.filter_by(fk_apartment=apart_req.id)
            for data in contract_req:
                contract_nbr = data.contract_nbr

            # Create PDF
            file = create_receipt_pdf(
                date_in=convert_date_to_string(request.form.get('date_in')),
                date_out=convert_date_to_string(request.form.get('date_out')),
                apartment='{} {} {}'.format(apart_req.address, str(apart_req.zipcode), apart_req.city),
                id_tenant=id_tenant
            )

            # Record receipt in DB
            receipt_req = Receipts(
                fk_apartment=request.form.get('apartment'),
                apartment_name=apart_req.apartment_name,
                name=name_tenant,
                lessor_id=0,
                tenant_id=int(id_tenant),
                added_date=datetime.date.today(),
                date_in=request.form.get('date_in'),
                date_out=request.form.get('date_out'),
                year=int(convert_to_year(request.form.get('date_in'))),
                month=convert_to_month(request.form.get('date_in')),
                price=apart_req.rent_price,
                loads=0,  # TODO add loads in apartments DB
                contract_nbr=contract_nbr,
                file_name=file
            )
            db.session.add(receipt_req)
            db.session.commit()

            # return send_from_directory(receipts_path, file)
            # return redirect(request.referrer)
            return redirect(url_for('receipts'))

        return render_template(
            'gestion_loc/receipts/form_receipt.html',
            form=form,
            title='Créer une Quittance',
            aparts=apartment_name_list,
            receipts=receipts_list
        )
    except Exception as e:
        print(e)
        return render_template(
            "error_404.html",
            log=e
        )


@app.route('/gestionLoc/receipts/edit_receipt<int:id_receipt>', methods=['GET', 'POST'])
@login_required
def edit_receipt(id_receipt):
    try:
        form = ReceiptForm()
        apartment_name_list = Apartments.query.all()
        receipts_list = Receipts.query.get_or_404(id_receipt)
        # TODO edit form to create
        # if request.method == 'POST':  # For Avio invoice
        #     # Get apartment_name
        #     req = Apartments.query.get_or_404(request.form.get('apartment'))
        #     # Record in DB invoice_out
        #     invoice_req = InvoicesOut(
        #         fk_apartment=request.form.get('apartment'),
        #         apartment_name=req.apartment_name,
        #         ref_customer=form.ref_customer.data,
        #         name=avio_json['name'],
        #         address=avio_json['address'],
        #         zipcode=avio_json['zipcode'],
        #         city=avio_json['city'],
        #         invoice_number=create_invoice_nbr(n=0, apart_name=get_apartment_name(request.form.get('apartment'))),
        #         added_date=datetime.date.today(),
        #         date_in=convert_date_string_to_isoformat(form.date_in.data),
        #         date_out=convert_date_string_to_isoformat(form.date_out.data),
        #         due_date=convert_date_string_to_isoformat(form.due_date.data),
        #         price=form.price.data,
        #         file_name='{}.pdf'.format(create_invoice_nbr(n=0, apart_name=get_apartment_name(request.form.get('apartment'))))
        #     )
        #     db.session.add(invoice_req)
        #     db.session.commit()
        #
        #     file = create_invoice_out_pdf(
        #         id_apart=request.form.get('apartment'),
        #         date_in=request.form.get('date_in'),
        #         date_out=request.form.get('date_out'),
        #         due_date=request.form.get('due_date'),
        #         price=form.price.data,
        #         ref_customer=form.ref_customer.data
        #     )
        #     # return send_from_directory(invoices_out_path, file)
        #     return redirect(url_for('receipts'))

        return render_template(
            'gestion_loc/receipts/form_receipt.html',
            form=form,
            title='Editer la Quittance',
            aparts=apartment_name_list,
            receipts=receipts_list
        )
    except Exception as e:
        print(e)
        return render_template(
            "error_404.html",
            log=e
        )


@app.route('/gestion_loc/receipts/download_receipt/<int:id_receipt>', methods=['GET', 'POST'])
@login_required
def download_receipt(id_receipt):
    try:
        # Get contract to download
        receipt_to_download = Receipts.query.get_or_404(id_receipt)
        return send_from_directory(receipts_path, receipt_to_download.file_name)

    except Exception as e:
        print(e)
        return render_template(
            "error_404.html",
            log=e
        )


@app.route('/gestionLoc/receipts/delete_receipt/<int:id_receipt>', methods=['GET', 'POST'])
@login_required
def delete_receipt(id_receipt):
    try:
        receipt_to_delete = Receipts.query.get_or_404(id_receipt)
        # Delete receipt of DB
        db.session.delete(receipt_to_delete)
        db.session.commit()
        # Delete file from receipts path
        os.remove(receipts_path + '/' + receipt_to_delete.file_name)
        flash('La quittance a bien été supprimé', category='success')
        return redirect(request.referrer)

    except Exception as e:
        print(e)
        return render_template(
            "error_404.html",
            log=e
        )

