import datetime
from flask_login import login_required
from soft import app, db
from flask import render_template, session, redirect, request, url_for, flash, send_from_directory

from soft.constant import parts_list_path
from soft.func.pdf_func import create_parts_pdf
from soft.saab.parts_list.forms import PartsListForm
from soft.saab.parts_list.model import PartsList
from soft.saab.tasks.model import JobCardList


@app.route('/saab/parts_list')
@login_required
def parts_list():
    req_parts_list = PartsList.query.all()
    return render_template(
        "saab/parts_list/parts_list.html",
        parts= req_parts_list
    )


@app.route('/saab/add_part', methods=['GET', 'POST'])
@login_required
def add_part():
    form = PartsListForm()
    form.job_card.choices = [i.item_jc for i in JobCardList.query.all()]

    if request.method == 'POST':
        try:
            part_to_add = PartsList(
            fk_job_card=form.job_card.data,
            description=form.description.data,
            pn=form.pn.data,
            sn=form.sn.data,
            qty=form.qty.data,
            reason=form.reason.data,
            remarks=form.remarks.data
            )
            db.session.add(part_to_add)
        except Exception as e:
            print(e)
            return redirect('parts_list')
        finally:
            db.session.commit()

            flash(f'The Part N°{form.pn.data} was added successfully !', category='success')
            return redirect('parts_list')

    return render_template(
        "saab/parts_list/form_parts_list.html",
        form=form,
        title="Add a Part"
    )


@app.route('/saab/edit_part<int:id_part>', methods=['GET', 'POST'])
@login_required
def edit_part(id_part):
    req_part = PartsList.query.get_or_404(id_part)
    form = PartsListForm(
        job_card=req_part.fk_job_card,
        description=req_part.description,
        pn=req_part.pn,
        sn=req_part.sn,
        qty=req_part.qty,
        reason=req_part.reason,
        remarks=req_part.remarks
    )

    if request.method == 'POST':
        try:
            req_part.fk_job_card = form.job_card.data
            req_part.description = form.description.data
            req_part.pn = form.pn.data
            req_part.sn = form.sn.data
            req_part.qty = form.qty.data
            req_part.reason = form.reason.data
            req_part.remarks = form.remarks.data
        except Exception as e:
            print(e)
            return redirect('parts_list')
        finally:
            db.session.commit()

            flash(f"The part N°{form.pn.data} was edited successfully !", category='success')
            return redirect('parts_list')

    return render_template(
        "saab/parts_list/form_parts_list.html",
        form=form,
        title="Edit Part"
    )


@app.route('/saab/delete_aprt<int:id_to_delete>', methods=['GET', 'POST'])
@login_required
def delete_part(id_to_delete):
    try:
        req_part_to_delete = PartsList.query.get_or_404(id_to_delete)
        db.session.delete(req_part_to_delete)
    except Exception as e:
        print(e)
        return redirect('parts_list')
    finally:
        db.session.commit()
        flash("The part was deleted successfully!", category='success')

    return redirect(request.referrer)


@app.route('/saab/print_parts_list', methods=['GET', 'POST'])
@login_required
def print_parts_list():
    checkbox_values = [
        request.form.get('check_all_parts'),
        request.form.get('check_removed_parts'),
        request.form.get('check_installed_parts')
    ]
    parts_list_to_print = []
    counter = 1
    if checkbox_values[0] is not None:  # All parts
        for i in PartsList.query.all():
            parts_row = [counter, i.description, i.pn,i.sn, i.qty, i.fk_job_card, i. reason, i.remarks]
            parts_list_to_print.append(parts_row)
            counter += 1
    elif checkbox_values[1] is not None:  # RRemoved parts
        for i in PartsList.query.filter_by(reason='Removed'):
            parts_row = [counter, i.description, i.pn,i.sn, i.qty, i.fk_job_card, i. reason, i.remarks]
            parts_list_to_print.append(parts_row)
            counter += 1
    elif checkbox_values[2] is not None:  # Installed parts
        for i in PartsList.query.filter_by(reason='Installed'):
            parts_row = [counter, i.description, i.pn,i.sn, i.qty, i.fk_job_card, i. reason, i.remarks]
            parts_list_to_print.append(parts_row)
            counter += 1

    filename = create_parts_pdf(
        parts_list=parts_list_to_print,
        checkbox_values=checkbox_values
    )
    return send_from_directory(
        parts_list_path,
        filename
    )