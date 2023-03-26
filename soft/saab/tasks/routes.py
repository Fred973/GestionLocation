import datetime
from flask_login import login_required
from soft import app, db
from flask import render_template, session, redirect, request, url_for, flash
from soft.saab.tasks.forms import JobCardListForm, JobCardDetailsForm
from soft.saab.tasks.model import JobCardList, JobCardDetails


@app.route('/SAAB/tasks_list', methods=['GET', 'POST'])
@login_required
def tasks_list():
    req_tasks_list = JobCardList.query.all()

    # Calculate the % of total accomplishment
    jc_counter = 0
    req_total_tasks_list = JobCardDetails.query.all()
    for i in req_total_tasks_list:
        if i.performed:
            jc_counter += 1
    try:
        total_accomplishment = round((jc_counter/len(req_total_tasks_list))*100)
    except ZeroDivisionError:
        total_accomplishment = 0

    # Calculate the % of accomplishment and total working time for each Job card
    for i in req_tasks_list:
        try:
            jc_counter = 0
            jc_performed_counter = 0
            jc_working_time = datetime.timedelta(0)

            job_card_req = JobCardDetails.query.filter_by(fk_task=i.id)
            for data in job_card_req:
                jc_counter += 1
                if data.performed:
                    jc_performed_counter += 1

                jc_working_time += datetime.timedelta(
                    hours=data.working_time.hour,
                    minutes=data.working_time.minute
                )

            i.accomplishment = round((jc_performed_counter/jc_counter)*100)
            i.working_time = jc_working_time
            db.session.commit()
        except ZeroDivisionError:
            i.accomplishment = 0
            db.session.commit()

    return render_template(
        'saab/tasks_list/tasks_list.html',
        job_cards=req_tasks_list,
        total_accomplishment=total_accomplishment
    )

@app.route('/SAAB/add_job_card', methods=['GET', 'POST'])
@login_required
def add_job_card():
    form = JobCardListForm()
    if request.method == 'POST':
        job_card_req = JobCardList(
            item_jc=form.item_jc.data,
            description=form.description.data,
            remarks=form.remarks.data,
            working_time=datetime.datetime.strptime('00:00', '%H:%M')
        )
        db.session.add(job_card_req)
        db.session.commit()
        flash('The Job card is saved successfully !', category='success')
        return redirect(url_for('tasks_list'))

    return render_template(
        'saab/tasks_list/form_job_card.html',
        title="Add Job card",
        form=form
    )

@app.route('/SAAB/edit_job_card<int:id_job_card>', methods=['GET', 'POST'])
@login_required
def edit_job_card(id_job_card):
    form = JobCardListForm()
    job_card_to_edit = JobCardList.query.get_or_404(id_job_card)

    if request.method == 'POST':
        job_card_to_edit.item_jc = form.item_jc.data
        job_card_to_edit.description = form.description.data
        # TODO see why remarks is not recorded on DB
        job_card_to_edit.remarks = form.remarks.data
        db.session.commit()

        flash('The Job Card was edited successfully !', category='success')
        return redirect(url_for('tasks_list'))

    form.item_jc.data = job_card_to_edit.item_jc
    form.description.data = job_card_to_edit.description
    form.remarks.data = job_card_to_edit.remarks

    return render_template(
        'saab/tasks_list/form_job_card.html',
        title='Edit Job card',
        form=form
    )

@app.route('/SAAB/job_card_deleting_page', methods=['GET', 'POST'])
@login_required
def job_card_deleting_page():
    req_tasks_list = JobCardList.query.all()

    return render_template(
        'saab/tasks_list/deleting_jc_list.html',
        job_cards=req_tasks_list
    )

@app.route('/SAAB/delete_job_card<int:id_to_delete>', methods=['GET', 'POST'])
@login_required
def delete_job_card(id_to_delete):
    job_card_to_delete = JobCardList.query.get_or_404(id_to_delete)
    db.session.delete(job_card_to_delete)
    db.session.commit()

    flash('The Job card (Work Order) and all related job cards (SAAB AMM) was deleted successfully !', category='success')
    return redirect(request.referrer)

@app.route('/SAAB/task_performed<int:id_job_card>', methods=['GET', 'POST'])
@login_required
def task_performed(id_job_card):
    job_card_to_update = JobCardDetails.query.get_or_404(id_job_card)
    job_card_to_update.performed = True
    db.session.commit()
    return redirect(request.referrer)

@app.route('/SAAB/undo_task_performed<int:id_job_card>', methods=['GET', 'POST'])
@login_required
def undo_task_performed(id_job_card):
    job_card_to_update = JobCardDetails.query.get_or_404(id_job_card)
    job_card_to_update.performed = False
    db.session.commit()
    return redirect(request.referrer)

@app.route('/SAAB/job_card_details<int:id_job_card>', methods=['GET', 'POST'])
@login_required
def show_job_card_details(id_job_card):
    jc_req = JobCardList.query.get_or_404(id_job_card)
    job_card_details_req = JobCardDetails.query.filter_by(fk_task=id_job_card).order_by(JobCardDetails.job_card.asc())

    session.pop('id_job_card', None)
    session.pop('job_card_nbr', None)
    session['id_job_card'] = id_job_card
    session['job_card_nbr'] = jc_req.item_jc
    return render_template(
        'saab/tasks_list/job_card_detail.html',
        id_jc=jc_req.item_jc,
        job_card_details=job_card_details_req
    )

@app.route('/SAAB/add_job_card_detail', methods=['GET', 'POST'])
@login_required
def add_job_card_detail():
    form = JobCardDetailsForm()
    if request.method == 'POST':
        job_card_req = JobCardDetails(
            fk_task=session['id_job_card'],
            job_card=form.job_card.data,
            type=form.type.data,
            mm_ref=form.mm_ref.data,
            description=form.description.data,
            remarks=form.remarks.data,
            working_time=form.working_time.data,
            nbr_tech=form.nbr_tech.data,
            performed=form.performed.data,
        )
        db.session.add(job_card_req)
        db.session.commit()
        flash('The task is successfully saved !', category='success')
        return redirect(url_for('show_job_card_details', id_job_card=session['id_job_card']))

    return render_template(
        'saab/tasks_list/form_task.html',
        title=f"Add Task to Job Card N°{session['job_card_nbr']}",
        form=form
    )

@app.route('/SAAB/edit_job_card_detail<int:id_job_card>', methods=['GET', 'POST'])
@login_required
def edit_job_card_detail(id_job_card):
    form = JobCardDetailsForm()
    task_to_edit = JobCardDetails.query.get_or_404(id_job_card)

    if request.method == 'POST':
        task_to_edit.job_card = form.job_card.data
        task_to_edit.type = form.type.data
        task_to_edit.mm_ref = form.mm_ref.data
        task_to_edit.description = form.description.data
        task_to_edit.remarks = form.remarks.data
        task_to_edit.working_time = form.working_time.data
        task_to_edit.nbr_tech = form.nbr_tech.data
        task_to_edit.performed = form.performed.data
        db.session.commit()

        flash('The Job Card was edited successfully !', category='success')
        return redirect(url_for('show_job_card_details', id_job_card=session['id_job_card']))

    form.job_card.data = task_to_edit.job_card
    form.type.data = task_to_edit.type
    form.mm_ref.data = task_to_edit.mm_ref
    form.description.data = task_to_edit.description
    form.remarks.data = task_to_edit.remarks
    form.working_time.data = task_to_edit.working_time
    form.nbr_tech.data = task_to_edit.nbr_tech
    form.performed.data = task_to_edit.performed

    return render_template(
        'saab/tasks_list/form_task.html',
        title=f"Edit Task N°{session['job_card_nbr']}",
        form=form
    )

@app.route('/SAAB/delete_job_card_detail<int:id_to_delete>', methods=['GET', 'POST'])
@login_required
def delete_job_card_detail(id_to_delete):
    job_card_to_delete = JobCardDetails.query.get_or_404(id_to_delete)
    db.session.delete(job_card_to_delete)
    db.session.commit()

    flash('The Task was deleted successfully !', category='success')
    return redirect(request.referrer)
