from flask_login import login_required, current_user
from soft import app, db
from flask import render_template, session, redirect, request, url_for, flash

from soft.experience.forms import TechLogForm
from soft.experience.model import TechLog


@app.route('/experiences/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard_exp():
    try:
        return render_template('experiences/dashboard_exp.html')
    except Exception as e:
        print(e)
        return render_template(
            "error_404.html",
            log=e
        )


@app.route('/experiences', methods=['GET', 'POST'])
@login_required
def experiences():
    try:
        techlog_req = TechLog.query.all()

        return render_template(
            'experiences/experiences.html',
            entries=techlog_req
        )
    except Exception as e:
        print(e)
        return render_template(
            "error_404.html",
            log=e
        )


@app.route('/TechLog/add_entry', methods=['GET', 'POST'])
@login_required
def add_entry():
    try:
        form = TechLogForm()

        if request.method == 'POST':
            entry_to_add = TechLog(
                date=form.date.data,
                ac_type=form.ac_type.data,
                registration=form.registration.data,
                ata=int(form.ata.data),
                work_order=form.work_order.data,
                description=form.description.data,
                work_type=form.work_type.data,
                time=form.time.data,
                function=form.function.data
            )
            db.session.add(entry_to_add)
            db.session.commit()

            flash("Entry added successfully !", category='success')

            return redirect(url_for('experiences'))

        return render_template(
            'experiences/entry_form.html',
            title='Add Entry',
            form=form
        )
    except Exception as e:
        print(e)
        return render_template(
            "error_404.html",
            log=e
        )


@app.route('/TechLog/edit_entry/<int:id_entry>', methods=['GET', 'POST'])
@login_required
def edit_entry(id_entry):
    try:
        form = TechLogForm()
        entry_to_edit = TechLog.query.get_or_404(id_entry)

        if request.method == 'POST':
            entry_to_edit.date = form.date.data
            entry_to_edit.ac_type = form.ac_type.data
            entry_to_edit.registration = form.registration.data
            entry_to_edit.ata = form.ata.data
            entry_to_edit.work_order = form.work_order.data
            entry_to_edit.description = form.description.data
            entry_to_edit.work_type = form.work_type.data
            entry_to_edit.time = form.time.data
            entry_to_edit.function = form.function.data

            db.session.commit()

            flash("Entry edited successfully !", category='success')

            return redirect(url_for('experiences'))

        form.date.data = entry_to_edit.date
        form.ac_type.data = entry_to_edit.ac_type
        form.registration.data = entry_to_edit.registration
        form.ata.data = entry_to_edit.ata
        form.work_order.data = entry_to_edit.work_order
        form.description.data = entry_to_edit.description
        form.work_type.data = entry_to_edit.work_type
        form.time.data = entry_to_edit.time
        form.function.data = entry_to_edit.function

        return render_template(
            'experiences/entry_form.html',
            title='Add Entry',
            form=form
        )
    except Exception as e:
        print(e)
        return render_template(
            "error_404.html",
            log=e
        )


@app.route('/TechLog/delete_entry/<int:id_entry>', methods=['GET', 'POST'])
@login_required
def delete_entry(id_entry):
    try:
        entry_to_delete = TechLog.query.get_or_404(id_entry)
        db.session.delete(entry_to_delete)
        db.session.commit()
        flash("Entry added successfully !", category='success')

        return redirect(url_for('experiences'))

    except Exception as e:
        print(e)
        return render_template(
            "error_404.html",
            log=e
        )