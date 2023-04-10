import datetime
from flask_login import login_required
from soft import app, db
from flask import render_template, session, redirect, request, url_for, flash
from soft.saab.equipment_list.forms import EquipmentListForm
from soft.saab.equipment_list.model import EquipmentList


@app.route('/SAAB/equipment_list', methods=['GET', 'POST'])
@login_required
def equipment_list():
    req_equipment_list = EquipmentList.query.all()
    return render_template(
        'saab/equipment_list/equipment_list.html',
        equipment_list=req_equipment_list
    )

@app.route('/SAAB/add_equipment', methods=['GET', 'POST'])
@login_required
def add_equipment():
    form = EquipmentListForm()
    if request.method == 'POST':
        equipment_req = EquipmentList(
            ata=form.ata.data,
            description=form.description.data,
            part_number=form.part_number.data,
            alternate_pn=form.alternate_pn.data,
            serial_number=form.serial_number.data,
            batch=form.batch.data,
            location=form.location.data,
            remarks=form.remarks.data
        )
        db.session.add(equipment_req)
        db.session.commit()
        flash('The equipment is saved successfully !', category='success')
        return redirect(url_for('equipment_list'))

    return render_template(
        'saab/equipment_list/form_equipment_list.html',
        title="Add Equipment",
        form=form
    )

@app.route('/SAAB/edit_equipment<int:id_equipment>', methods=['GET', 'POST'])
@login_required
def edit_equipment(id_equipment):
    form = EquipmentListForm()
    equipment_to_edit = EquipmentList.query.get_or_404(id_equipment)

    if request.method == 'POST':
        equipment_to_edit.ata = form.ata.data
        equipment_to_edit.part_number = form.part_number.data
        equipment_to_edit.alternate_pn = form.alternate_pn.data
        equipment_to_edit.serial_number = form.serial_number.data
        equipment_to_edit.batch = form.batch.data
        equipment_to_edit.location = form.location.data
        equipment_to_edit.description = form.description.data
        equipment_to_edit.remarks = form.remarks.data
        db.session.commit()
        flash('The equipment is saved successfully !', category='success')
        return redirect(url_for('equipment_list'))

    form.ata.data = equipment_to_edit.ata
    form.part_number.data = equipment_to_edit.part_number
    form.description.data = equipment_to_edit.description
    form.serial_number.data = equipment_to_edit.serial_number
    form.alternate_pn.data = equipment_to_edit.alternate_pn
    form.batch.data = equipment_to_edit.batch
    form.location.data = equipment_to_edit.location
    form.remarks.data = equipment_to_edit.remarks

    return render_template(
        'saab/equipment_list/form_equipment_list.html',
        title="Edit Equipment",
        form=form
    )

@app.route('/SAAB/delete_equipment<int:id_to_delete>', methods=['GET', 'POST'])
@login_required
def delete_equipment(id_to_delete):
    equipment_to_delete = EquipmentList.query.get_or_404(id_to_delete)
    db.session.delete(equipment_to_delete)
    db.session.commit()

    flash('The equipment was deleted successfully !', category='success')
    return redirect(request.referrer)
