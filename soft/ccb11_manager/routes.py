from flask_login import login_required, current_user
from soft import app, db
from flask import render_template, session, redirect, request, url_for, flash
from soft.ccb11_manager.forms import TaskForm
from soft.ccb11_manager.model import Tasks
from soft.login.model import Users


@app.route('/CCB11/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard_CCB():
    try:
        user_req = Users.query.get_or_404(current_user.id)

        return render_template(
            'CCB11/dashboard.html',
            user=user_req
        )
    except Exception as e:
        print(e)
        return render_template(
            "error_404.html",
            log=e
        )


@app.route('/GestionLocation/dashboard_GL', methods=['GET', 'POST'])
@login_required
def return_dashboard_GL():
    session['id_choice'] = 0
    return redirect(url_for('dashboard_GL'))


@app.route('/CCB11/dashboard_CCB', methods=['GET', 'POST'])
@login_required
def return_dashboard_CCB():
    session['id_choice'] = 1
    return redirect(url_for('dashboard_CCB'))


@app.route('/CCB11/Tasks', methods=['GET', 'POST'])
@login_required
def tasks():

    return render_template(
        'CCB11/tasks.html',
        tasks=Tasks.query.order_by(Tasks.id.desc()).all()
    )


@app.route('/CCB11/AddTasks', methods=['GET', 'POST'])
@login_required
def add_task():
    form = TaskForm()

    if request.method == 'POST':
        if (request.form.get('closed_date')) == '':
            closed_date = None
        else:
            closed_date = request.form.get('closed_date')
        task_req = Tasks(
            type=request.form.get('type'),
            description=form.description.data,
            added_date=request.form.get('added_date'),
            relevance=request.form.get('relevance'),
            closed_date=closed_date,
            remarks=form.remarks.data,
            status=form.status.data
        )
        db.session.add(task_req)
        db.session.commit()

        flash('The task is added successfully !', category='success')
        return redirect(url_for('tasks'))

    return render_template(
        'CCB11/form_task.html',
        title='Add Task',
        form=form
    )


@app.route('/CCB11/EditTasks<int:id_task>', methods=['GET', 'POST'])
@login_required
def edit_task(id_task):
    form = TaskForm()
    # Get data from DB
    task_to_edit = Tasks.query.get_or_404(id_task)

    if request.method == 'POST':
        task_to_edit.type = form.type.data
        task_to_edit.description = form.description.data
        task_to_edit.added_date = form.added_date.data
        task_to_edit.relevance = form.relevance.data
        task_to_edit.closed_date = form.closed_date.data
        task_to_edit.remarks = form.remarks.data
        task_to_edit.status = form.status.data
        db.session.commit()

        flash('The task was updated successfully !', category='success')
        return redirect(url_for('tasks'))

    form.type.data = task_to_edit.type
    form.description.data = task_to_edit.description
    form.added_date.data = task_to_edit.added_date
    form.relevance.data = task_to_edit.relevance
    form.closed_date.data = task_to_edit.closed_date
    form.remarks.data = task_to_edit.remarks
    form.status.data = task_to_edit.status

    return render_template(
        'CCB11/form_task.html',
        title='Edit Task',
        form=form
    )


@app.route('/CCB11/DeleteTasks<int:id_task>', methods=['GET', 'POST'])
@login_required
def delete_task(id_task):
    task_to_delete = Tasks.query.get_or_404(id_task)
    db.session.delete(task_to_delete)
    db.session.commit()
    flash('The task was deleteed successfully !', category='success')
    return redirect(request.referrer)