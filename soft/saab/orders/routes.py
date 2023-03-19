import datetime
from flask_login import login_required, current_user, login_user
from soft import app, db
from flask import render_template, session, redirect, request, url_for, flash, send_from_directory

from soft.constant import orders_path
from soft.func.db_func import get_all_orders, get_received_orders, get_ordered_orders
from soft.func.pdf_func import create_orders_pdf
from soft.saab.orders.forms import OrderListForm
from soft.saab.orders.model import OrderList

@app.route('/SAAB/orders_list', methods=['GET', 'POST'])
@login_required
def orders_list():
    req_order_list = OrderList.query.all()
    return render_template(
        'saab/orders_list/orders_list.html',
        orders=req_order_list
    )

@app.route('/SAAB/add_orders_list', methods=['GET', 'POST'])
@login_required
def add_orders_list():
    form = OrderListForm()
    if request.method == 'POST':
        order_req = OrderList(
            part_number=form.part_number.data,
            description=form.description.data,
            qty=form.qty.data,
            remark=form.remark.data,
            job_card=form.job_card.data,
            order_sent_on=form.order_sent_on.data,
            received=False,
            record_by=current_user.name,
            creation_date=datetime.date.today()
        )
        db.session.add(order_req)
        db.session.commit()
        flash('The order is saved successfully !', category='success')
        return redirect(url_for('orders_list'))

    return render_template(
        'saab/orders_list/form_orders_list.html',
        title="Add order",
        form=form
    )

@app.route('/SAAB/edit_orders_list<int:id_order>', methods=['GET', 'POST'])
@login_required
def edit_orders_list(id_order):
    form = OrderListForm()
    order_to_edit = OrderList.query.get_or_404(id_order)

    if request.method == 'POST':
        order_to_edit.part_number = form.part_number.data
        order_to_edit.description = form.description.data
        order_to_edit.qty = form.qty.data
        order_to_edit.job_card = form.job_card.data
        order_to_edit.order_sent_on = form.order_sent_on.data
        order_to_edit.remark = form.remark.data
        order_to_edit.record_by = current_user.name
        order_to_edit.creation_date = datetime.date.today()
        db.session.commit()

        flash('The order was edited successfully !', category='success')
        return redirect(url_for('orders_list'))

    form.part_number.data = order_to_edit.part_number
    form.description.data = order_to_edit.description
    form.qty.data = order_to_edit.qty
    form.remark.data = order_to_edit.remark
    form.job_card.data = order_to_edit.job_card
    form.order_sent_on.data = order_to_edit.order_sent_on

    return render_template(
        'saab/orders_list/form_orders_list.html',
        title='Edit Order',
        form=form
    )

@app.route('/SAAB/order_received<int:id_order>', methods=['GET', 'POST'])
@login_required
def order_received(id_order):
    order_req = OrderList.query.get_or_404(id_order)
    order_req.received = True
    order_req.received_on = datetime.date.today()
    db.session.commit()

    flash('The order status is changed to received', category='success')
    return redirect(request.referrer)

@app.route('/SAAB/undo_received<int:id_order>', methods=['GET', 'POST'])
@login_required
def undo_received(id_order):
    order_req = OrderList.query.get_or_404(id_order)
    order_req.received = False
    order_req.received_on = None
    db.session.commit()

    flash('The order status is changed to not received', category='success')
    return redirect(request.referrer)

@app.route('/SAAB/delete_orders_list<int:id_to_delete>', methods=['GET', 'POST'])
@login_required
def delete_orders_list(id_to_delete):
    question_to_delete = OrderList.query.get_or_404(id_to_delete)
    db.session.delete(question_to_delete)
    db.session.commit()

    flash('The order was deleted successfully !', category='success')
    return redirect(request.referrer)

@app.route('/SAAB/print_orders', methods=['GET', 'POST'])
@login_required
def print_to_pdf():
    checkbox_values = [
        request.form.get('check_all_orders'),
        request.form.get('check_received_orders'),
        request.form.get('check_ordered_orders')
    ]
    orders_list_to_print = []
    counter = 1
    if checkbox_values[0] is not None:  # All orders
        for i in get_all_orders():
            orders_row = [counter, i.part_number, i.description, i.qty, i.job_card, i. order_sent_on, i.record_by, i.creation_date]
            orders_list_to_print.append(orders_row)
            counter += 1
    elif checkbox_values[1] is not None:  # Received orders
        for i in get_received_orders():
            orders_row = [counter, i.part_number, i.description, i.qty, i.job_card, i. order_sent_on, i.record_by, i.creation_date]
            orders_list_to_print.append(orders_row)
            counter += 1
    elif checkbox_values[2] is not None:  # Ordered orders
        for i in get_ordered_orders():
            orders_row = [counter, i.part_number, i.description, i.qty, i.job_card, i. order_sent_on, i.record_by, i.creation_date]
            orders_list_to_print.append(orders_row)
            counter += 1

    filename = create_orders_pdf(
        orders_list=orders_list_to_print,
        checkbox_values=checkbox_values
    )
    return send_from_directory(
        orders_path,
        filename
    )