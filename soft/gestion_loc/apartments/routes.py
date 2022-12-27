from flask import render_template, flash, redirect, url_for, request
from flask_login import login_required

from soft import app, db
from soft.gestion_loc.apartments.forms import ApartmentForm
from soft.gestion_loc.apartments.model import Apartments


@app.route('/gestionLoc/Apartments', methods=['GET', 'POST'])
@login_required
def apartments():
    try:
        apartment_list = Apartments.query.all()
    except Exception as e:
        print(e)
        return render_template(
            "error_404.html",
            log=e
        )

    return render_template(
        "gestion_loc/apartments/apartments.html",
        aparts=apartment_list
    )


@app.route('/gestionLoc/Apartments/add_Apartment', methods=['GET', 'POST'])
@login_required
def add_apartment():
    try:
        form = ApartmentForm()
        if form.validate_on_submit():
            if form.month_day.data == 'Par Jour':
                month = False
                day = True
            else:
                month = True
                day = False
            apart_to_add = Apartments(
                apartment_name=form.apartment_name.data,
                address=form.address.data,
                zipcode=form.zipcode.data,
                city=form.city.data,
                rent_price=form.rent_price.data,
                month=month,
                day=day
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
    except Exception as e:
        print(e)
        return render_template(
            "error_404.html",
            log=e
        )


@app.route('/gestionLoc/Apartments/edit_apartment/<int:id_apart>', methods=['GET', 'POST'])
@login_required
def edit_apartment(id_apart):
    try:
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
    except Exception as e:
        print(e)
        return render_template(
            "error_404.html",
            log=e
        )


@app.route('/gestionLoc/Apartments/delete_apartment/<int:id_apart>', methods=['GET'])
@login_required
def delete_apartment(id_apart):
    try:
        apart_to_delete = Apartments.query.get_or_404(id_apart)
        db.session.delete(apart_to_delete)
        db.session.commit()
        flash("L'appartement a bien été supprimé", category='success')
        return redirect(request.referrer)
    except Exception as e:
        print(e)
        return render_template(
            "error_404.html",
            log=e
        )
