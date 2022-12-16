from flask import render_template, request, flash, redirect, url_for
from flask_login import login_required

from soft import app, db
from soft.gestion_loc.tenants.forms import TenantForm
from soft.gestion_loc.apartments.model import Apartments
from soft.gestion_loc.tenants.model import Tenants


@app.route('/gestionLoc/Tenants', methods=['GET', 'POST'])
@login_required
def tenants():
    try:
        tenants_list = Tenants.query.all()

        return render_template(
            "gestion_loc/tenants/tenants.html",
            tenants=tenants_list
        )
    except Exception as e:
        print(e)
        return render_template(
            "error_404.html",
            log=e
        )


@app.route('/gestionLoc/Tenants/add_tenant', methods=['GET', 'POST'])
@login_required
def add_tenant():
    try:
        form = TenantForm()
        apartment_name_list = Apartments.query.all()
        if request.method == "POST":
            # Get apartment_name
            req = Apartments.query.get_or_404(request.form.get('apartment'))

            tenant_req = Tenants(
                fk_apartment=request.form.get('apartment'),
                apartment_name=req.apartment_name,
                first_name=form.first_name.data,
                name=form.name.data,
                phone=form.phone.data,
                email=form.email.data
            )
            db.session.add(tenant_req)
            db.session.commit()

            flash('Le locataire a bien été ajouté !', category='success')
            return redirect(url_for('tenants'))

        return render_template(
            "gestion_loc/tenants/form_tenant.html",
            title='Ajouter un locataire',
            aparts=apartment_name_list,
            form=form
        )
    except Exception as e:
        print(e)
        return render_template(
            "error_404.html",
            log=e
        )


@app.route('/gestionLoc/Tenants/edit_tenant<int:id_tenant>', methods=['GET', 'POST'])
@login_required
def edit_tenant(id_tenant):
    try:
        form = TenantForm()
        tenant_to_edit = Tenants.query.get_or_404(id_tenant)
        apartment_name_list = Apartments.query.all()

        if request.method == 'POST':
            tenant_to_edit.name = form.name.data
            tenant_to_edit.first_name = form.first_name.data
            tenant_to_edit.phone = form.phone.data
            tenant_to_edit.email = form.email.data
            db.session.commit()

            # Clear the form
            form.name.data = ''
            form.first_name.data = ''
            form.phone.data = ''
            form.email.data = ''

            flash('Le Locataire a bien été modifié', category='success')
            return redirect(url_for('tenants'))

        form.name.data = tenant_to_edit.name
        form.first_name.data = tenant_to_edit.first_name
        form.phone.data = tenant_to_edit.phone
        form.email.data = tenant_to_edit.email
        return render_template(
            "gestion_loc/tenants/form_tenant.html",
            title='Modifier',
            form=form,
            aparts=apartment_name_list
        )
    except Exception as e:
        print(e)
        return render_template(
            "error_404.html",
            log=e
        )


@app.route('/gestionLoc/Tenants/delete_tenant/<int:id_tenant>', methods=['GET'])
@login_required
def delete_tenant(id_tenant):
    try:
        tenant_to_delete = Tenants.query.get_or_404(id_tenant)
        # Delete contract of DB
        db.session.delete(tenant_to_delete)
        db.session.commit()

        flash('Le locataire a bien été supprimé', category='success')
        return redirect(request.referrer)
    except Exception as e:
        print(e)
        return render_template(
            "error_404.html",
            log=e
        )
